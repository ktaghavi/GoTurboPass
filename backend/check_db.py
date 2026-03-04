"""
check_db.py — GoTurboPass database diagnostic script.

Verifies that all migrations ran cleanly, all expected tables exist,
key columns are present (especially migration-added ones), and seed
data (58 CA counties + courts) is intact.

Usage (from backend/ with venv active):
    python check_db.py
"""

import sys
from sqlalchemy import inspect, text

# ── Bootstrap Flask app context ────────────────────────────────────────────────
from app import create_app
from models import db

app = create_app()

# ── Expected schema ground truth ───────────────────────────────────────────────
EXPECTED_TABLES = [
    "alembic_version",
    "audit_logs",
    "certificates",
    "citations",
    "counties",
    "courts",
    "exam_attempts",
    "exams",
    "inquiries",
    "modules",
    "payments",
    "progress",
    "questions",
    "quizzes",
    "student_profiles",
    "users",
]

# Columns that were ADDED by the compliance migration (not in original schema).
# If any are missing the migration did not fully apply.
MIGRATION_SENTINEL_COLUMNS = {
    "student_profiles": ["dl_hash", "dl_last4"],
    "users":            ["email_verified_at"],
    "exams":            ["duration_seconds"],
    "exam_attempts":    ["expires_at", "answer_order"],
}

# dl_number must be GONE (it was dropped and replaced)
DROPPED_COLUMNS = {
    "student_profiles": ["dl_number"],
}

EXPECTED_ALEMBIC_HEAD = "96ebe6f7b4e1"

EXPECTED_COUNTY_COUNT = 58  # all 58 CA counties

# ── Helpers ────────────────────────────────────────────────────────────────────
PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
WARN = "\033[93m⚠\033[0m"
INFO = "\033[94m•\033[0m"


def banner(title: str) -> None:
    width = 70
    print()
    print("─" * width)
    print(f"  {title}")
    print("─" * width)


def row(status: str, label: str, detail: str = "") -> None:
    suffix = f"  ({detail})" if detail else ""
    print(f"  {status}  {label}{suffix}")


# ── Main checks ────────────────────────────────────────────────────────────────
errors: list[str] = []
warnings: list[str] = []


def run_checks() -> None:
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = set(inspector.get_table_names())

        # ── 1. Alembic version ─────────────────────────────────────────────────
        banner("1 · Alembic Migration State")
        if "alembic_version" not in existing_tables:
            row(FAIL, "alembic_version table missing — migrations never ran")
            errors.append("alembic_version table missing")
        else:
            result = db.session.execute(text("SELECT version_num FROM alembic_version")).fetchall()
            heads = [r[0] for r in result]
            if EXPECTED_ALEMBIC_HEAD in heads:
                row(PASS, f"Current head: {heads[0]}")
            else:
                row(FAIL, f"Expected head {EXPECTED_ALEMBIC_HEAD!r}, got {heads}")
                errors.append(f"Wrong alembic head: {heads}")

        # ── 2. Table presence ──────────────────────────────────────────────────
        banner("2 · Table Presence")
        for table in sorted(EXPECTED_TABLES):
            if table in existing_tables:
                row(PASS, table)
            else:
                row(FAIL, f"{table}  ← MISSING")
                errors.append(f"Missing table: {table}")

        extra = existing_tables - set(EXPECTED_TABLES)
        if extra:
            row(WARN, f"Extra tables (not in expected list): {sorted(extra)}")
            warnings.append(f"Extra tables: {sorted(extra)}")

        # ── 3. Row counts ──────────────────────────────────────────────────────
        banner("3 · Row Counts")
        countable = [t for t in sorted(EXPECTED_TABLES) if t != "alembic_version"]
        for table in countable:
            if table not in existing_tables:
                row(WARN, f"{table:<25} skipped (table missing)")
                continue
            count = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            row(INFO, f"{table:<25} {count:>6} row(s)")

        # ── 4. Migration sentinel columns ──────────────────────────────────────
        banner("4 · Migration-Added Columns")
        for table, cols in MIGRATION_SENTINEL_COLUMNS.items():
            if table not in existing_tables:
                row(WARN, f"{table} — table missing, skipping column checks")
                continue
            existing_cols = {c["name"] for c in inspector.get_columns(table)}
            for col in cols:
                if col in existing_cols:
                    row(PASS, f"{table}.{col}")
                else:
                    row(FAIL, f"{table}.{col}  ← MISSING")
                    errors.append(f"Missing column: {table}.{col}")

        # ── 5. Dropped columns (must NOT exist) ────────────────────────────────
        banner("5 · Dropped Columns (must be absent)")
        for table, cols in DROPPED_COLUMNS.items():
            if table not in existing_tables:
                continue
            existing_cols = {c["name"] for c in inspector.get_columns(table)}
            for col in cols:
                if col not in existing_cols:
                    row(PASS, f"{table}.{col} correctly absent")
                else:
                    row(FAIL, f"{table}.{col} still present — migration may not have run")
                    errors.append(f"Column should be dropped but exists: {table}.{col}")

        # ── 6. Full column listing ─────────────────────────────────────────────
        banner("6 · Column Listing per Table")
        for table in sorted(existing_tables):
            cols = [c["name"] for c in inspector.get_columns(table)]
            print(f"\n  [{table}]")
            for col in cols:
                print(f"      {col}")

        # ── 7. Seed data integrity ─────────────────────────────────────────────
        banner("7 · Seed Data Integrity")

        if "counties" not in existing_tables:
            row(FAIL, "counties table missing — cannot check seed data")
            errors.append("counties table missing for seed check")
        else:
            county_count = db.session.execute(
                text("SELECT COUNT(*) FROM counties")
            ).scalar()

            if county_count == EXPECTED_COUNTY_COUNT:
                row(PASS, f"counties: {county_count} rows (expected {EXPECTED_COUNTY_COUNT})")
            elif county_count == 0:
                row(FAIL, f"counties: 0 rows — run: python seed_geo_full.py")
                errors.append("counties table is empty — seed not run")
            else:
                row(WARN, f"counties: {county_count} rows (expected {EXPECTED_COUNTY_COUNT})")
                warnings.append(f"Unexpected county count: {county_count}")

        if "courts" not in existing_tables:
            row(FAIL, "courts table missing — cannot check seed data")
            errors.append("courts table missing for seed check")
        else:
            court_count = db.session.execute(
                text("SELECT COUNT(*) FROM courts")
            ).scalar()

            if court_count == 0:
                row(FAIL, "courts: 0 rows — run: python seed_geo_full.py")
                errors.append("courts table is empty — seed not run")
            else:
                row(PASS, f"courts: {court_count} rows")

            # Counties with NO courts attached
            if "counties" in existing_tables and county_count > 0:
                orphan_counties = db.session.execute(text("""
                    SELECT c.name
                    FROM   counties c
                    LEFT JOIN courts ct ON ct.county_id = c.id
                    WHERE  ct.id IS NULL
                    ORDER BY c.name
                """)).fetchall()
                if orphan_counties:
                    names = [r[0] for r in orphan_counties]
                    row(WARN, f"Counties with 0 courts: {names}")
                    warnings.append(f"Counties with no courts: {names}")
                else:
                    row(PASS, "All counties have at least one court")

        # ── 8. Summary ─────────────────────────────────────────────────────────
        banner("8 · Summary")
        if not errors and not warnings:
            print(f"\n  {PASS}  All checks passed — database looks healthy.\n")
        else:
            if errors:
                print(f"\n  {FAIL}  {len(errors)} error(s):")
                for e in errors:
                    print(f"        • {e}")
            if warnings:
                print(f"\n  {WARN}  {len(warnings)} warning(s):")
                for w in warnings:
                    print(f"        • {w}")
            print()

        sys.exit(1 if errors else 0)


if __name__ == "__main__":
    run_checks()

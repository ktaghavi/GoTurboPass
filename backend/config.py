"""
Application configuration.

All sensitive values come from environment variables.
Never commit real credentials — use a local .env file (gitignored)
and inject secrets via your hosting platform in production.

See .env.example for every required variable and its description.
"""
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class Config:
    # ── Flask ─────────────────────────────────────────────────────────────────
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-CHANGE-IN-PRODUCTION")
    FLASK_ENV  = os.getenv("FLASK_ENV", "development")
    DEBUG      = FLASK_ENV == "development"

    # ── Database ──────────────────────────────────────────────────────────────
    # Production: set DATABASE_URL to your PostgreSQL URI
    # Local dev:  spin up Docker Postgres (see README) or set DATABASE_URL
    # SQLite fallback is for initial bootstrapping ONLY — not production-safe
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'goturbopass_dev.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = FLASK_ENV == "development"

    # ── JWT ───────────────────────────────────────────────────────────────────
    JWT_SECRET_KEY           = os.getenv("JWT_SECRET", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_ALGORITHM            = "HS256"
    JWT_TOKEN_LOCATION       = ["headers"]
    JWT_HEADER_NAME          = "Authorization"
    JWT_HEADER_TYPE          = "Bearer"

    # ── CORS ──────────────────────────────────────────────────────────────────
    FRONTEND_ORIGINS = [
        o.strip()
        for o in os.getenv(
            "FRONTEND_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
    ]

    # ── Rate limiting ─────────────────────────────────────────────────────────
    # Swap to Redis URI for production: redis://:<pw>@<host>:6379/0
    RATELIMIT_STORAGE_URL     = os.getenv("RATELIMIT_STORAGE_URL", "memory://")
    RATELIMIT_DEFAULT         = "200 per hour"
    RATELIMIT_HEADERS_ENABLED = True

    # ── Security headers / CSP ────────────────────────────────────────────────
    CSP_POLICY = (
        "default-src 'self'; "
        "script-src 'self' https://js.stripe.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "connect-src 'self' https://api.stripe.com; "
        "frame-src https://js.stripe.com; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self';"
    )

    # ── SMTP (stubbed — wire a real provider before going live) ───────────────
    SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
    SMTP_FROM = os.getenv("SMTP_FROM", "noreply@goturbopass.com")

    # ── DMV compliance constants ───────────────────────────────────────────────
    # Total required instructional time: exactly 340 minutes = 20,400 seconds
    REQUIRED_TOTAL_SECONDS  = int(os.getenv("REQUIRED_TOTAL_SECONDS", "20400"))

    # Default per-module minimum (340 min / 12 modules = 1,700 s ≈ 28.3 min)
    # Individual modules may override via Module.min_seconds column.
    DEFAULT_MODULE_SECONDS  = int(os.getenv("DEFAULT_MODULE_SECONDS", "1700"))

    # Server-side heartbeat fraud detection
    HEARTBEAT_INTERVAL      = int(os.getenv("HEARTBEAT_INTERVAL", "30"))   # expected client interval
    HEARTBEAT_GRACE_SECONDS = int(os.getenv("HEARTBEAT_GRACE_SECONDS", "35"))  # max allowed gap

    # Final exam
    EXAM_DURATION_SECONDS   = int(os.getenv("EXAM_DURATION_SECONDS", "3600"))  # 60 min
    EXAM_PASS_PERCENT       = int(os.getenv("EXAM_PASS_PERCENT", "70"))
    MAX_EXAM_ATTEMPTS       = int(os.getenv("MAX_EXAM_ATTEMPTS", "3"))

    # Module quizzes
    QUIZ_PASS_PERCENT       = int(os.getenv("QUIZ_PASS_PERCENT", "70"))

    # Instructor inquiry SLA (hours)
    SLA_HOURS               = int(os.getenv("SLA_HOURS", "24"))

    # ── Stripe ────────────────────────────────────────────────────────────────
    STRIPE_SECRET_KEY        = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET    = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    STRIPE_PRICE_CENTS       = int(os.getenv("STRIPE_PRICE_CENTS", "500"))  # $5.00

    # ── School identity (certificates + TVCC submission) ─────────────────────
    SCHOOL_NAME              = os.getenv("SCHOOL_NAME", "GoTurboPass Online Traffic School")
    SCHOOL_DMV_NUMBER        = os.getenv("SCHOOL_DMV_NUMBER", "PENDING")

    # ── PII redaction list (keys matched case-insensitively in AuditService) ──
    PII_FIELDS = {
        "password", "passwordhash", "password_hash",
        "cadlnumber", "ca_dl_number", "dl_number", "dlnumber",
        "dob", "ssn",
    }

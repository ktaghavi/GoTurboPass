# backend/migrations/env.py
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
import os, sys
from pathlib import Path

# --- Put backend/ on sys.path early so relative imports work ---
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# --- Load environment variables so DATABASE_URL is available ---
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except Exception:
    pass

# --- Alembic config object (define BEFORE using it) ---
config = context.config

# --- Configure logging from alembic.ini if present ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Set the DB URL on the alembic config ---
db_url = os.getenv("DATABASE_URL")
if not db_url:
    # Optional fallback to your app config if you keep it
    try:
        from config import Config
        db_url = getattr(Config, "SQLALCHEMY_DATABASE_URI", None)
    except Exception:
        db_url = None
if not db_url:
    raise RuntimeError("DATABASE_URL not set (and no fallback found).")

config.set_main_option("sqlalchemy.url", db_url)

# --- Import models AFTER path/env are ready so metadata is populated ---
from models.db import db
from models import Module, Quiz, User, Progress, Certificate, AuditLog, Exam, Inquiry  # noqa: F401

target_metadata = db.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration with security defaults."""

    # Flask
    SECRET_KEY = os.getenv('JWT_SECRET', 'dev-secret-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql+psycopg2://user:pass@localhost:5432/goturbopass'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = FLASK_ENV == 'development'

    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_ALGORITHM = 'HS256'

    # CORS
    FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173')

    # Rate Limiting
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_DEFAULT = "100 per hour"
    RATELIMIT_HEADERS_ENABLED = True

    # Security Headers (CSP)
    CSP_POLICY = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        f"connect-src 'self' {os.getenv('FRONTEND_ORIGIN', 'http://localhost:5173')}; "
        "frame-ancestors 'none'; "
        "base-uri 'none';"
    )

    # SMTP (stub for Phase 1)
    SMTP_HOST = os.getenv('SMTP_HOST', 'localhost')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 1025))

    # Business Logic
    SLA_HOURS = int(os.getenv('SLA_HOURS', 24))
    MODULE_TIMER_SECONDS = int(os.getenv('MODULE_TIMER_SECONDS', 600))
    QUIZ_PASS_PERCENT = int(os.getenv('QUIZ_PASS_PERCENT', 70))
    EXAM_PASS_PERCENT = int(os.getenv('EXAM_PASS_PERCENT', 70))

    # PII Redaction - fields to never log
    PII_FIELDS = {'emai', 'caDlNumber', 'dob', 'password', 'ca_dl_hash', 'ca_dl_full'}
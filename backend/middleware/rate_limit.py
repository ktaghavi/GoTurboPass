"""
Rate limiter factory.

Uses Flask-Limiter backed by in-memory storage for development.
For production, swap RATELIMIT_STORAGE_URL to a Redis URI:
  redis://:<password>@<host>:6379/0
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_limiter() -> Limiter:
    """Return a configured Limiter instance (not yet bound to an app)."""
    return Limiter(
        key_func=get_remote_address,
        default_limits=["200 per hour"],
        storage_uri="memory://",
        headers_enabled=True,          # Exposes X-RateLimit-* headers
        swallow_errors=True,           # Don't 500 on limiter backend errors
    )

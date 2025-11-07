from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_limiter():
    """Create and configure Flask-Limiter."""
    return Limiter(
        key_func=get_remote_address,
        default_limits=["100 per hour"],
        storage_uri="memory://",
        headers_enabled=True,
    )

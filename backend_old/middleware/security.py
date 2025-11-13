from flask import Response
from config import Config


def apply_security_headers(response: Response) -> Response:
    """
    Apply security headers to all responses.

    - CSP (Content Security Policy)
    - X-Content-Type-Options
    - X-Frame-Options
    - X-XSS-Protection
    - Strict-Transport-Security (HTTPS only)
    """
    # Content Security Policy
    response.headers['Content-Security-Policy'] = Config.CSP_POLICY

    # Prevent MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'

    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'

    # XSS Protection (legacy, but still good practice)
    response.headers['X-XSS-Protection'] = '1; mode=block'

    # HSTS (only in production with real TLS)
    if Config.FLASK_ENV == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    return response

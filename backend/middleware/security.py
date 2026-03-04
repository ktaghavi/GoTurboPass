"""
Security headers middleware.

Applied to every response via app.after_request.
Headers enforced:
  - Content-Security-Policy
  - X-Content-Type-Options (MIME sniffing prevention)
  - X-Frame-Options       (clickjacking prevention)
  - X-XSS-Protection      (legacy browsers)
  - Strict-Transport-Security (HTTPS only; production flag-gated)
"""
from flask import Response


def apply_security_headers(response: Response, config) -> Response:
    """Inject security headers into every outgoing response."""

    response.headers["Content-Security-Policy"] = config.get(
        "CSP_POLICY", "default-src 'self';"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # HSTS only when TLS is present (production)
    if getattr(config, "FLASK_ENV", "development") == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )

    return response

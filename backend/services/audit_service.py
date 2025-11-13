from models.db import db
from models.audit_log import AuditLog
from flask import request
from config import Config
from datetime import datetime
import traceback


class AuditService:
    """Audit logging service with PII redaction."""

    @staticmethod
    def log_event(event: str, student_id=None, user_id=None, details=None):
        """
        Log an audit event with PII redaction.
        Never raises exceptions — failures are logged & rolled back.
        """
        try:
            # Redact PII
            safe_details = AuditService._redact_pii(details) if details else {}

            # Safe extraction of request context
            ip = getattr(request, "remote_addr", None)
            user_agent = request.headers.get("User-Agent") if request else None

            # Create audit log entry
            log = AuditLog(
                event=event,
                student_id=student_id,
                user_id=user_id,
                ip=ip,
                user_agent=user_agent,
                details=safe_details,
                created_at=datetime.utcnow(),
            )

            db.session.add(log)
            db.session.commit()

        except Exception:
            db.session.rollback()
            traceback.print_exc()  # keep this for dev visibility; remove in prod

    @staticmethod
    def _redact_pii(data: dict) -> dict:
        """Return a shallow copy with configured PII fields redacted."""
        if not isinstance(data, dict):
            return data
        redacted = data.copy()
        for field in getattr(Config, "PII_FIELDS", []):
            if field in redacted:
                redacted[field] = "[REDACTED]"
        return redacted
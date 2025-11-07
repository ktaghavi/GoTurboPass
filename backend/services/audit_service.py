from models import db
from models.audit_log import AuditLog
from flask import request
from config import Config


class AuditService:
    """Audit logging service with PII redaction."""

    @staticmethod
    def log_event(
        event: str,
        student_id: int = None,
        user_id: int = None,
        details: dict = None
    ):
        """
        Log an audit event with PII redaction.

        Args:
            event: Event name (e.g., 'REGISTER', 'LOGIN', 'TIMER_START')
            student_id: Student ID (if applicable)
            user_id: User ID (generic, if applicable)
            details: Additional context (will be PII-redacted)
        """
        # Redact PII from details
        safe_details = AuditService._redact_pii(details) if details else None

        # Extract IP and User-Agent from request context
        ip = request.remote_addr if request else None
        user_agent = request.headers.get('User-Agent') if request else None

        # Create audit log entry
        log = AuditLog(
            event=event,
            student_id=student_id,
            user_id=user_id,
            ip=ip,
            user_agent=user_agent,
            details=safe_details
        )
        db.session.add(log)
        db.session.commit()

    @staticmethod
    def _redact_pii(data: dict) -> dict:
        """Redact PII fields from dict."""
        if not isinstance(data, dict):
            return data

        redacted = data.copy()
        for field in Config.PII_FIELDS:
            if field in redacted:
                redacted[field] = '[REDACTED]'
        return redacted

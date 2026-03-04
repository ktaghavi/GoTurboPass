"""
AuditLog — compliance trail for CA DMV audit requirements.

Every event that touches course state, authentication, or student PII
must be written here via AuditService.log_event().  This table is
append-only by policy — no row should ever be updated or deleted.

See services/audit_service.py for the full list of standard event names.
"""
from datetime import datetime, timezone

from models.db import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    # Who performed the action (null for pre-auth events like LOGIN_FAIL)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    event = db.Column(db.String(100), nullable=False, index=True)

    # Network context (IPv4 or IPv6)
    ip = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)

    # Arbitrary PII-redacted payload (stored as JSON)
    details = db.Column(db.JSON, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    def __repr__(self):
        return f"<AuditLog {self.id} {self.event} student={self.student_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "event": self.event,
            "ip": self.ip,
            "user_agent": self.user_agent,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

from .db import db
from sqlalchemy.orm import relationship
from datetime import datetime


class AuditLog(db.Model):
    """
    Audit log for security and compliance tracking.

    Events: REGISTER, LOGIN, VERIFY_EMAIL, TIMER_START, TIMER_END,
            QUIZ_SUBMIT, EXAM_SUBMIT, CERT_GENERATE, etc.
    """
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    user_id = db.Column(db.Integer, nullable=True)  # Generic user reference

    event = db.Column(db.String(100), nullable=False, index=True)
    ip = db.Column(db.String(45), nullable=True)  # IPv4/IPv6
    user_agent = db.Column(db.String(500), nullable=True)
    details = db.Column(db.JSON, nullable=True)  # Additional context (PII-redacted)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<AuditLog {self.id} {self.event}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'user_id': self.user_id,
            'event': self.event,
            'ip': self.ip,
            'user_agent': self.user_agent,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

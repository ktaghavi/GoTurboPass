from models import db
from datetime import datetime
from enum import Enum


class InquiryStatus(str, Enum):
    """Inquiry status enumeration."""
    OPEN = "OPEN"
    ANSWERED = "ANSWERED"
    EXPIRED = "EXPIRED"


class Inquiry(db.Model):
    """
    Student inquiry to instructor (24h SLA).
    """
    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    module_context = db.Column(db.String(255), nullable=True)  # Optional module reference

    # Status & SLA
    status = db.Column(db.Enum(InquiryStatus), nullable=False, default=InquiryStatus.OPEN, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    answered_at = db.Column(db.DateTime, nullable=True)
    handled_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Instructor/Admin

    # Relationships
    handled_by = db.relationship('User', foreign_keys=[handled_by_id], backref='handled_inquiries')

    def __repr__(self):
        return f'<Inquiry {self.id} {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'body': self.body,
            'module_context': self.module_context,
            'status': self.status.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'answered_at': self.answered_at.isoformat() if self.answered_at else None,
            'handled_by_id': self.handled_by_id,
        }

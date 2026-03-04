"""
Inquiry — student question to instructor (24-hour SLA).

CA DMV OL-613 requires that students have access to an instructor
for questions during the course.  Each inquiry must be answered within
24 hours.  Unanswered inquiries past the SLA are marked EXPIRED and
trigger an alert to the admin dashboard.

Statuses:
  OPEN      — submitted, not yet answered
  ANSWERED  — instructor replied within SLA
  EXPIRED   — SLA elapsed without an answer (compliance risk flag)
"""
from datetime import datetime, timezone
from enum import Enum

from models.db import db


class InquiryStatus(str, Enum):
    OPEN     = "OPEN"
    ANSWERED = "ANSWERED"
    EXPIRED  = "EXPIRED"


class Inquiry(db.Model):
    __tablename__ = "inquiries"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)

    # Optional reference to the module the student was viewing
    module_context = db.Column(db.String(255), nullable=True)

    # Status & SLA tracking
    status = db.Column(
        db.Enum(InquiryStatus),
        nullable=False,
        default=InquiryStatus.OPEN,
        index=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    answered_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Instructor or admin who answered
    handled_by_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    answer_body = db.Column(db.Text, nullable=True)

    # Relationships
    student = db.relationship(
        "User",
        foreign_keys=[student_id],
        back_populates="inquiries",
    )
    handled_by = db.relationship(
        "User",
        foreign_keys=[handled_by_id],
    )

    def __repr__(self):
        return f"<Inquiry {self.id} [{self.status}] student={self.student_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject": self.subject,
            "body": self.body,
            "module_context": self.module_context,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "answered_at": self.answered_at.isoformat() if self.answered_at else None,
            "handled_by_id": self.handled_by_id,
            "answer_body": self.answer_body,
        }

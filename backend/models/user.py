"""
User — authentication and identity for all roles.

Roles: STUDENT | INSTRUCTOR | ADMIN

PII handling:
  • password_hash  — werkzeug pbkdf2; never logged, never serialized
  • dob            — used for certificate; excluded from to_dict() by default
  • Driver License — NOT stored here; see StudentProfile (dl_hash, dl_last4)
"""
from datetime import datetime, timezone

from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash

from models.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # ── Auth ──────────────────────────────────────────────────────────────────
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email_verified_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # ── Role ──────────────────────────────────────────────────────────────────
    role = db.Column(db.String(20), nullable=False, default="STUDENT")

    # ── Identity ──────────────────────────────────────────────────────────────
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    profile = db.relationship(
        "StudentProfile", back_populates="user", uselist=False
    )
    citations = db.relationship(
        "Citation", back_populates="user", lazy="dynamic"
    )
    payments = db.relationship(
        "Payment", back_populates="user", lazy="dynamic"
    )
    progress_records = db.relationship(
        "Progress",
        back_populates="student",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    exam_attempts = db.relationship(
        "ExamAttempt",
        back_populates="student",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    certificates = db.relationship(
        "Certificate",
        back_populates="student",
        lazy="dynamic",
    )
    inquiries = db.relationship(
        "Inquiry",
        foreign_keys="Inquiry.student_id",
        back_populates="student",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    # ── Auth helpers ──────────────────────────────────────────────────────────
    def set_password(self, plain: str) -> None:
        self.password_hash = generate_password_hash(plain)

    def check_password(self, plain: str) -> bool:
        return check_password_hash(self.password_hash, plain)

    @staticmethod
    def normalize_email(raw: str) -> str:
        valid = validate_email(raw, check_deliverability=False)
        return valid.email

    # ── Computed helpers ──────────────────────────────────────────────────────
    @property
    def full_name(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    @property
    def email_verified(self) -> bool:
        return self.email_verified_at is not None

    def has_paid(self) -> bool:
        """Return True if this student has at least one confirmed payment."""
        from models.payment import PaymentStatus
        return (
            self.payments.filter_by(status=PaymentStatus.PAID).first()
        ) is not None

    def total_verified_seconds(self) -> int:
        """Sum of verified timer_seconds across all progress records."""
        from sqlalchemy import func
        from models.progress import Progress
        result = (
            db.session.query(func.sum(Progress.timer_seconds))
            .filter(Progress.student_id == self.id)
            .scalar()
        )
        return result or 0

    # ── Serialization ─────────────────────────────────────────────────────────
    def to_dict(self, include_pii: bool = False) -> dict:
        """
        Safe serialization for API responses.
        password_hash is NEVER included.
        """
        data = {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_verified": self.email_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_pii:
            data["dob"] = self.dob.isoformat() if self.dob else None
        return data

    def __repr__(self):
        return f"<User {self.id} {self.email} ({self.role})>"

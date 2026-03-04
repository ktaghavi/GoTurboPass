"""
StudentProfile — extended enrollment data collected during registration.

PII handling — Driver License:
  The full DL number is NEVER stored in plaintext.
  On enrollment the DL is processed by AuthService:
    dl_hash  = AuthService.hash_dl(raw_dl)     # bcrypt, one-way
    dl_last4 = AuthService.extract_dl_last4(raw_dl)  # last 4 for certificate

  TVCC NOTE: The TVCC API requires the full DL number at submission time.
  Since we cannot reverse dl_hash, options are:
    (a) Ask the student to re-enter the DL at TVCC submission time, OR
    (b) Add a separately AES-encrypted dl_encrypted column in a future sprint.
  This is flagged in routes/tvcc_stub.py.
"""
from datetime import datetime, timezone
from enum import Enum

from models.db import db


class GenderEnum(str, Enum):
    MALE     = "MALE"
    FEMALE   = "FEMALE"
    NONBINARY = "NONBINARY"


class DLClassEnum(str, Enum):
    A     = "A"
    B     = "B"
    C     = "C"
    M     = "M"
    OTHER = "OTHER"


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ── Identity ──────────────────────────────────────────────────────────────
    first_name = db.Column(db.String(100), nullable=True)
    last_name  = db.Column(db.String(100), nullable=True)
    gender     = db.Column(db.Enum(GenderEnum), nullable=True)
    dob        = db.Column(db.Date, nullable=True)

    # ── Contact ───────────────────────────────────────────────────────────────
    phone  = db.Column(db.String(20),  nullable=True)
    street = db.Column(db.String(255), nullable=True)
    city   = db.Column(db.String(255), nullable=True)
    state  = db.Column(db.String(2),   nullable=True)   # e.g. 'CA'
    zip    = db.Column(db.String(10),  nullable=True)

    # ── Driver's License — PII-protected ─────────────────────────────────────
    # dl_number is NEVER stored in plaintext.
    dl_hash  = db.Column(db.String(255), nullable=True)  # bcrypt hash of full DL
    dl_last4 = db.Column(db.String(4),   nullable=True)  # last 4 chars (certificate display)
    dl_state = db.Column(db.String(2),   nullable=True)  # issuing state
    dl_class = db.Column(db.Enum(DLClassEnum), nullable=True)

    # ── Marketing ─────────────────────────────────────────────────────────────
    how_found = db.Column(db.String(255), nullable=True)

    # ── Timestamps ────────────────────────────────────────────────────────────
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    user = db.relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<StudentProfile {self.id} user={self.user_id}>"

from datetime import datetime
from enum import Enum
from models.db import db


class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NONBINARY = "NONBINARY"


class DLClassEnum(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    M = "M"
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

    # Identity
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.Enum(GenderEnum), nullable=True)
    dob = db.Column(db.Date, nullable=True)

    # Contact
    phone = db.Column(db.String(20), nullable=True)
    street = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(2), nullable=True)  # e.g. 'CA'
    zip = db.Column(db.String(10), nullable=True)

    # Driver’s License
    dl_number = db.Column(db.String(50), nullable=True)
    dl_state = db.Column(db.String(2), nullable=True)   # 'CA' for now
    dl_class = db.Column(db.Enum(DLClassEnum), nullable=True)

    # Marketing
    how_found = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = db.relationship("User", back_populates="profile")

from .db import db
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    STUDENT = "STUDENT"
    INSTRUCTOR = "INSTRUCTOR"
    ADMIN = "ADMIN"
    REVIEWER = "REVIEWER"


class User(db.Model):
    """
    User model for all roles (STUDENT, INSTRUCTOR, ADMIN, REVIEWER).

    PII Security:
    - ca_dl_hash: Full CA DL number hashed + salted (bcrypt)
    - ca_dl_last4: Last 4 digits only (for certificate display)
    - dob: Date of birth (never logged)
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.STUDENT)

    # Contact & Auth
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email_verified_at = db.Column(db.DateTime, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Personal Info
    full_name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=True)  # Required for STUDENT

    # CA Driver License (PII protected)
    ca_dl_hash = db.Column(db.String(255), nullable=True)  # bcrypt hash of full DL
    ca_dl_last4 = db.Column(db.String(4), nullable=True)   # Last 4 for certificate

    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    progress = db.relationship('Progress', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    exam_attempts = db.relationship('ExamAttempt', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    certificates = db.relationship('Certificate', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    inquiries = db.relationship('Inquiry', foreign_keys='Inquiry.student_id', backref='student', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.id} {self.email} ({self.role})>'

    def to_dict(self, include_pii=False):
        """Safe serialization - excludes password_hash and ca_dl_hash by default."""
        data = {
            'id': self.id,
            'role': self.role.value,
            'email': self.email,
            'email_verified': self.email_verified_at is not None,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_pii:
            data['ca_dl_last4'] = self.ca_dl_last4
            data['dob'] = self.dob.isoformat() if self.dob else None
        return data

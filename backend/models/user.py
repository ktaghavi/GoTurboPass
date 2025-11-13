from datetime import datetime, date
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash, check_password_hash

from models.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Basic auth
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Role (for future admin dashboard, etc.)
    role = db.Column(db.String(20), nullable=False, default="STUDENT")  # STUDENT | ADMIN

    # Name + DOB (duplicated into StudentProfile is fine)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    profile = db.relationship("StudentProfile", back_populates="user", uselist=False)
    citations = db.relationship("Citation", back_populates="user", lazy="dynamic")

    def set_password(self, plain: str):
        self.password_hash = generate_password_hash(plain)

    def check_password(self, plain: str) -> bool:
        return check_password_hash(self.password_hash, plain)

    @staticmethod
    def normalize_email(raw: str) -> str:
        valid = validate_email(raw, check_deliverability=False)
        return valid.email

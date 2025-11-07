import bcrypt
from flask_jwt_extended import create_access_token
from datetime import datetime


class AuthService:
    """Authentication service for password and DL hashing, JWT creation."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against bcrypt hash."""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @staticmethod
    def hash_ca_dl(dl_number: str) -> str:
        """
        Hash full CA DL number using bcrypt (for PII protection).
        This allows verification without storing plaintext.
        """
        return bcrypt.hashpw(dl_number.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def extract_dl_last4(dl_number: str) -> str:
        """Extract last 4 characters of DL for certificate display."""
        return dl_number[-4:] if len(dl_number) >= 4 else dl_number

    @staticmethod
    def create_jwt(user_id: int, role: str) -> str:
        """Create JWT access token."""
        identity = {'user_id': user_id, 'role': role}
        return create_access_token(identity=identity)

    @staticmethod
    def generate_email_verification_token(email: str) -> str:
        """Generate email verification token (stub for Phase 1)."""
        # In production, use itsdangerous.URLSafeTimedSerializer
        return bcrypt.hashpw(email.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')[:32]

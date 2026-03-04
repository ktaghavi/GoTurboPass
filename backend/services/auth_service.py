"""
AuthService — DL hashing and JWT creation.

NOTE on password hashing:
  Passwords are hashed via werkzeug.security (User.set_password / check_password).
  We do NOT duplicate that here. AuthService handles only:
    • CA Driver License number hashing (bcrypt, one-way PII protection)
    • JWT access token creation

NOTE on DL storage strategy:
  We store:
    dl_hash  — bcrypt hash of the full DL (proves we received it; cannot be reversed)
    dl_last4 — plaintext last-4 characters (used on the certificate display)

  The full DL number is NOT stored in any recoverable form.
  For TVCC API submission the student must re-enter their DL at submission time,
  OR a separate AES-encrypted field (dl_encrypted) must be added in a future sprint.
  This is flagged in routes/tvcc_stub.py when that module is built.
"""
import bcrypt
from flask_jwt_extended import create_access_token


class AuthService:

    @staticmethod
    def hash_dl(dl_number: str) -> str:
        """
        Hash a CA driver license number with bcrypt.
        One-way — cannot be reversed. Used to prove we stored the DL
        without exposing it in a breach.
        """
        return bcrypt.hashpw(
            dl_number.strip().encode("utf-8"),
            bcrypt.gensalt(rounds=12),
        ).decode("utf-8")

    @staticmethod
    def extract_dl_last4(dl_number: str) -> str:
        """Return the last 4 characters of the DL for certificate display."""
        cleaned = dl_number.strip()
        return cleaned[-4:] if len(cleaned) >= 4 else cleaned

    @staticmethod
    def create_jwt(user_id: int, role: str) -> str:
        """
        Create a signed JWT access token.
        Expiry is controlled by JWT_ACCESS_TOKEN_EXPIRES in config.
        """
        return create_access_token(
            identity={"user_id": user_id, "role": role}
        )

"""
Auth routes — registration and login.

POST /api/auth/register       Create a new student account (email + password only).
                              Personal info and DL are collected via POST /api/enroll.
POST /api/auth/login          Authenticate and return a JWT access token.
POST /api/auth/forgot-password  Stub — Phase 4 will wire up SMTP reset flow.

Rate limits (enforced at app.py via the limiter instance):
  register: 10/hour/IP   — prevents mass account farming
  login:    10/min/IP    — prevents brute-force attacks
"""
from flask import Blueprint, request, jsonify
from email_validator import EmailNotValidError

from models.db import db
from models.user import User
from services.auth_service import AuthService
from services.audit_service import AuditService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# ── Register ──────────────────────────────────────────────────────────────────

@auth_bp.route("/register", methods=["POST", "OPTIONS"])
def register():
    """
    Create a new student account.
    Accepts: { email, password }
    Returns: { userId, message }
    """
    if request.method == "OPTIONS":
        return ("", 204)

    if not request.is_json:
        return jsonify({"error": "Expected application/json"}), 415

    data     = request.get_json(silent=True) or {}
    email    = (data.get("email") or "").strip()
    password = data.get("password") or ""

    missing = []
    if not email:    missing.append("email")
    if not password: missing.append("password")
    if missing:
        return jsonify({"error": "Missing required fields", "missing": missing}), 400

    try:
        email = User.normalize_email(email)
    except EmailNotValidError:
        return jsonify({"error": "Invalid email address"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    try:
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        AuditService.log_event("REGISTER", student_id=user.id)

        return jsonify({
            "userId": user.id,
            "message": "Registration successful",
        }), 201

    except Exception:
        db.session.rollback()
        import traceback; traceback.print_exc()
        return jsonify({"error": "Registration failed"}), 500


# ── Login ─────────────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    """
    Authenticate a student and return a short-lived JWT.
    Accepts: { email, password }
    Returns: { accessToken, user: { id, email, full_name, role, email_verified } }

    Always returns 401 with a generic message on bad credentials —
    never hint which field was wrong (prevents username enumeration).
    """
    if request.method == "OPTIONS":
        return ("", 204)

    if not request.is_json:
        return jsonify({"error": "Expected application/json"}), 415

    data     = request.get_json(silent=True) or {}
    email    = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        AuditService.log_event("LOGIN_FAIL")
        return jsonify({"error": "Invalid email or password"}), 401

    token = AuthService.create_jwt(user_id=user.id, role=user.role)
    AuditService.log_event("LOGIN", student_id=user.id)

    return jsonify({
        "accessToken": token,
        "user": user.to_dict(),
    }), 200


# ── Password reset stub (Phase 4) ─────────────────────────────────────────────

@auth_bp.route("/forgot-password", methods=["POST", "OPTIONS"])
def forgot_password():
    """
    Stub: accept an email, always return 200 to prevent email enumeration.
    Phase 4 will wire up itsdangerous token + SMTP dispatch.
    """
    if request.method == "OPTIONS":
        return ("", 204)
    return jsonify({
        "message": "If that email is registered you will receive a reset link shortly."
    }), 200

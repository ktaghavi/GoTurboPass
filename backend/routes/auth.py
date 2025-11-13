from flask import Blueprint, request, jsonify
from models.db import db
from models.user import User
from email_validator import EmailNotValidError

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST", "OPTIONS"])
def register():
    # CORS preflight
    if request.method == "OPTIONS":
        return ("", 204)

    if not request.is_json:
        return jsonify({"error": "Expected application/json"}), 415

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""

    missing = []
    if not email:
        missing.append("email")
    if not password:
        missing.append("password")

    if missing:
        return jsonify({"error": "Missing required fields", "missing": missing}), 400

    # Normalize & validate email
    try:
        email = User.normalize_email(email)
    except EmailNotValidError:
        return jsonify({"error": "Invalid email address"}), 400

    # Check existing user
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    # Create and save
    try:
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "userId": user.id,
            "message": "Registration successful"
        }), 201
    except Exception as e:
        db.session.rollback()
        # For now, print to console so we can see what went wrong
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Registration failed"}), 500

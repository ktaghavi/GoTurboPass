"""
/api/me — return the currently authenticated student's profile.

Used by the frontend AuthContext on page load (if a token is available)
and by the Dashboard to render user info.

GET /api/me
  Headers: Authorization: Bearer <token>
  Returns: { user: {...}, profile: {...} | null, has_paid: bool, total_seconds: int }
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User

me_bp = Blueprint("me", __name__)


@me_bp.route("/api/me", methods=["GET"])
@jwt_required()
def get_me():
    identity = get_jwt_identity()
    user = User.query.get(identity["user_id"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    profile = user.profile
    profile_data = None
    if profile:
        profile_data = {
            "first_name":  profile.first_name,
            "last_name":   profile.last_name,
            "dob":         profile.dob.isoformat() if profile.dob else None,
            "phone":       profile.phone,
            "street":      profile.street,
            "city":        profile.city,
            "state":       profile.state,
            "zip":         profile.zip,
            "dl_last4":    profile.dl_last4,
            "dl_state":    profile.dl_state,
            "dl_class":    profile.dl_class.value if profile.dl_class else None,
            "gender":      profile.gender.value if profile.gender else None,
        }

    return jsonify({
        "user":           user.to_dict(),
        "profile":        profile_data,
        "has_paid":       user.has_paid(),
        "total_seconds":  user.total_verified_seconds(),
    }), 200

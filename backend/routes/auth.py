from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, date

from models.db import db
from models.user import User, UserRole
from services.auth_service import AuthService
from services.audit_service import AuditService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    # Debug logs — good to keep at the very top
    print("Origin:", request.headers.get("Origin"))
    print("Method:", request.method)
    print("CT:", request.headers.get("Content-Type"))
    print("JSON(preview):", request.get_json(silent=True))

    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return ('', 204)

    try:
        # Require JSON and guard against None
        if not request.is_json:
            return jsonify({'error': 'Expected application/json'}), 415

        data = request.get_json(silent=True) or {}

        # Validate required fields with a clear message
        required = ['fullName', 'email', 'dob', 'caDlNumber', 'password']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({'error': 'Missing required fields', 'missing': missing}), 400

        # Validate email
        try:
            valid = validate_email(data['email'], check_deliverability=False)
            email = valid.email
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email address'}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        # Parse DOB
        try:
            dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format (use YYYY-MM-DD)'}), 400

        # Hash password
        password_hash = AuthService.hash_password(data['password'])

        # Hash CA DL and extract last 4
        ca_dl_hash = AuthService.hash_ca_dl(data['caDlNumber'])
        ca_dl_last4 = AuthService.extract_dl_last4(data['caDlNumber'])

        # Create user
        user = User(
            role=UserRole.STUDENT,
            email=email,
            password_hash=password_hash,
            full_name=data['fullName'],
            dob=dob,
            ca_dl_hash=ca_dl_hash,
            ca_dl_last4=ca_dl_last4,
            email_verified_at=None
        )
        db.session.add(user)
        db.session.commit()

        # Audit log (PII redacted)
        AuditService.log_event(
            event='REGISTER',
            student_id=user.id,
            details={'email': email, 'role': user.role.value}
        )

        # Phase 1 stub: return a verification token
        verification_token = AuthService.generate_email_verification_token(email)

        return jsonify({
            'userId': user.id,
            'message': 'Registration successful. Please verify your email.',
            'verificationToken': verification_token
        }), 201

    except Exception as e:
        db.session.rollback()
        # Log full traceback server-side
        import traceback; traceback.print_exc()
        return jsonify({'error': 'Registration failed'}), 500
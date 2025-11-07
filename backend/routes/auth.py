from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, date

from models import db
from models.user import User, UserRole
from services.auth_service import AuthService
from services.audit_service import AuditService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user (STUDENT by default).

    Body:
        {
            "fullName": str,
            "email": str,
            "dob": str (YYYY-MM-DD),
            "caDlNumber": str,
            "password": str
        }

    Returns:
        { "userId": int, "message": str }

    Security:
        - Full CA DL is hashed using bcrypt
        - Only last 4 stored plainly
        - Password is bcrypt hashed
        - PII fields never logged
    """
    try:
        data = request.get_json()

        # Validate required fields
        required = ['fullName', 'email', 'dob', 'caDlNumber', 'password']
        if not all(field in data for field in required):
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate email
        try:
            valid = validate_email(data['email'])
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
            email_verified_at=None  # Requires verification
        )
        db.session.add(user)
        db.session.commit()

        # Audit log (PII redacted)
        AuditService.log_event(
            event='REGISTER',
            student_id=user.id,
            details={'email': email, 'role': user.role.value}
        )

        # TODO Phase 2: Send verification email
        # For now, return token in response (stub)
        verification_token = AuthService.generate_email_verification_token(email)

        return jsonify({
            'userId': user.id,
            'message': 'Registration successful. Please verify your email.',
            'verificationToken': verification_token  # Phase 1 stub
        }), 201

    except Exception as e:
        db.session.rollback()
        # Generic error message (don't leak details)
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/verify', methods=['POST'])
def verify_email():
    """
    Verify email address (stub for Phase 1).

    Body:
        { "token": str }

    Returns:
        { "message": str }
    """
    try:
        data = request.get_json()
        token = data.get('token')

        if not token:
            return jsonify({'error': 'Token required'}), 400

        # Phase 1 stub: Accept any token for testing
        # TODO Phase 2: Implement itsdangerous token verification
        # For now, just mark first unverified user as verified (demo only)
        user = User.query.filter_by(email_verified_at=None).first()
        if user:
            user.email_verified_at = datetime.utcnow()
            db.session.commit()

            AuditService.log_event(
                event='VERIFY_EMAIL',
                student_id=user.id,
                details={'email': user.email}
            )

            return jsonify({'message': 'Email verified successfully'}), 200

        return jsonify({'error': 'Invalid or expired token'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Verification failed'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login and receive JWT access token.

    Body:
        { "email": str, "password": str }

    Returns:
        { "accessToken": str, "user": {...} }
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        # Find user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Verify password
        if not AuthService.verify_password(password, user.password_hash):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Check email verification (required for STUDENT role)
        if user.role == UserRole.STUDENT and not user.email_verified_at:
            return jsonify({'error': 'Email not verified. Please check your inbox.'}), 403

        # Create JWT
        access_token = AuthService.create_jwt(user.id, user.role.value)

        # Audit log
        AuditService.log_event(
            event='LOGIN',
            student_id=user.id if user.role == UserRole.STUDENT else None,
            user_id=user.id,
            details={'email': email, 'role': user.role.value}
        )

        return jsonify({
            'accessToken': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user info from JWT (protected route test).

    Returns:
        { "user": {...} }
    """
    try:
        identity = get_jwt_identity()
        user_id = identity.get('user_id')

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'user': user.to_dict(include_pii=True)}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve user'}), 500

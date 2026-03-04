"""
GoTurboPass — Flask application factory.

After pulling this revision, run the one-time setup in your WSL terminal:
  cd backend
  source venv/bin/activate
  pip install -r requirements.txt
  flask db init                                  # creates migrations/ directory
  flask db migrate -m "initial compliance schema"
  flask db upgrade                               # applies schema to the database
  python seed_geo_full.py                        # seed CA counties + courts
"""
import traceback

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from config import Config
from models import db
from middleware.security import apply_security_headers
from middleware.rate_limit import create_limiter

from routes.auth       import auth_bp
from routes.geo        import geo_bp
from routes.enrollment import enrollment_bp
from routes.me         import me_bp

jwt     = JWTManager()
migrate = Migrate()
limiter = create_limiter()


def create_app(config_class=Config):
    """Application factory — returns a fully configured Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Extensions ────────────────────────────────────────────────────────────
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # ── CORS ──────────────────────────────────────────────────────────────────
    CORS(
        app,
        origins=app.config["FRONTEND_ORIGINS"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

    # ── Security headers on every response ────────────────────────────────────
    @app.after_request
    def add_security_headers(response):
        return apply_security_headers(response, app.config)

    # ── Blueprints ────────────────────────────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(geo_bp)
    app.register_blueprint(enrollment_bp)
    app.register_blueprint(me_bp)

    # Tighter rate limits on auth mutations (applied after blueprint registration)
    limiter.limit("10 per hour",   methods=["POST"])(auth_bp)
    limiter.limit("10 per minute", methods=["POST"])(auth_bp)

    # ── Health check ──────────────────────────────────────────────────────────
    @app.get("/health")
    def health():
        return jsonify({"status": "healthy", "env": app.config["FLASK_ENV"]}), 200

    # ── JWT error handlers ────────────────────────────────────────────────────
    @jwt.unauthorized_loader
    def missing_token(_reason):
        return jsonify({"error": "Missing or invalid token"}), 401

    @jwt.invalid_token_loader
    def invalid_token(_reason):
        return jsonify({"error": "Invalid token"}), 401

    @jwt.expired_token_loader
    def expired_token(_header, _payload):
        return jsonify({"error": "Token has expired"}), 401

    # ── Global error handler ──────────────────────────────────────────────────
    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            return e
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

    # NOTE: db.create_all() has been REMOVED.
    # Schema is managed exclusively via Flask-Migrate (Alembic).
    # Run `flask db upgrade` to apply all migrations before first launch.

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
    
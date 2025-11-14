from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from models import db
from routes.auth import auth_bp
from routes.geo import geo_bp
from routes.enrollment import enrollment_bp
from werkzeug.exceptions import HTTPException
import traceback


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init DB
    db.init_app(app)

    # CORS
    CORS(
        app,
        origins=app.config.get("FRONTEND_ORIGINS", ["http://localhost:5173", "http://127.0.0.1:5173"]),
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(geo_bp)
    app.register_blueprint(enrollment_bp)

    # Health check
    @app.get("/health")
    def health():
        return jsonify({"status": "healthy"}), 200

    # Error handling
    @app.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            return e
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

    # Create tables automatically in dev (no migrations yet)
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
    
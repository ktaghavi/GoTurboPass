from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from models.db import db
from middleware.security import apply_security_headers
from middleware.rate_limit import create_limiter
from routes.auth import auth_bp


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    limiter = create_limiter()
    limiter.init_app(app)

    # CORS - locked to frontend origin
    CORS(app, origins=[app.config['FRONTEND_ORIGIN']], supports_credentials=True)

    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        return apply_security_headers(response)

    # Register blueprints
    app.register_blueprint(auth_bp)

    # Apply rate limiting to auth routes
    limiter.limit("10 per minute")(auth_bp)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'}), 200

    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'GoTurboPass API',
            'version': '1.0.0',
            'env': app.config['FLASK_ENV']
        }), 200

    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return jsonify({'error': 'Missing or invalid token'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({'error': 'Invalid token'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401

    # Generic error handler
    @app.errorhandler(Exception)
    def handle_error(e):
        # Log error (but not to client for security)
        app.logger.error(f'Unhandled error: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config['FLASK_ENV'] == 'development')

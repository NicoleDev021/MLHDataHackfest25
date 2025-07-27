from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, session

from app.config import config
from app.logging_config import setup_logging

oauth = OAuth()


def create_app(config_name="default"):
    # Load environment variables from .env file
    load_dotenv(find_dotenv())

    app = Flask(__name__)

    # Load configuration
    config_class = config.get(config_name, config["default"])
    
    # Initialize URL configuration before loading config
    config_class.init_urls()
    
    app.config.from_object(config_class)
    app.secret_key = app.config["SECRET_KEY"]

    # Setup logging
    setup_logging(app)
    app.logger.info(f"Starting application with {config_name} configuration")

    # Configure secure session settings
    app.config.update(
        SESSION_COOKIE_SECURE=app.config.get("FLASK_ENV") == "production",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=3600,  # 1 hour in seconds
    )

    # Validate Auth0 configuration
    required_auth0_vars = ["AUTH0_CLIENT_ID", "AUTH0_CLIENT_SECRET", "AUTH0_DOMAIN"]
    missing_vars = [var for var in required_auth0_vars if not app.config.get(var)]
    if missing_vars:
        raise RuntimeError(f"Missing Auth0 configuration: {', '.join(missing_vars)}")

    # Initialize OAuth
    oauth.init_app(app)
    oauth.register(
        "auth0",
        client_id=app.config["AUTH0_CLIENT_ID"],
        client_secret=app.config["AUTH0_CLIENT_SECRET"],
        api_base_url=f"https://{app.config['AUTH0_DOMAIN']}",
        access_token_url=f"https://{app.config['AUTH0_DOMAIN']}/oauth/token",
        authorize_url=f"https://{app.config['AUTH0_DOMAIN']}/authorize",
        jwks_uri=f"https://{app.config['AUTH0_DOMAIN']}/.well-known/jwks.json",
        client_kwargs={
            "scope": "openid profile email",
            "response_type": "code",
            "token_endpoint_auth_method": "client_secret_post",
        },
    )

    # Register error handlers
    register_error_handlers(app)

    # Add root route
    @app.route("/")
    def home():
        user_authenticated = session.get("user") is not None
        return render_template(
            "home.html",
            user_authenticated=user_authenticated,
            username=(
                session.get("profile", {}).get("name") if user_authenticated else None
            ),
        )

    # Register the auth blueprint with correct import
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    app.logger.info("Application initialization completed")
    return app


def register_error_handlers(app):
    """Register error handlers for the application."""

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("errors/403.html"), 403

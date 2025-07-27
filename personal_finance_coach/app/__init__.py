"""
Flask application factory and configuration module.

This module provides the main application factory function and handles:
- Flask application initialization
- OAuth2 configuration with Auth0
- Security settings and session management
- Error handlers registration
- Blueprint registration
"""

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, session

from app.config import config
from app.logging_config import setup_logging

oauth = OAuth()


def create_app(config_name="default"):
    """
    Flask application factory function.

    This is the heart of the application - it creates and configures a Flask app
    instance. Using the "Application Factory Pattern" allows us to:
    - Create multiple app instances for testing
    - Configure apps differently for dev/production
    - Keep configuration separate from application logic
    - Make the app more modular and testable

    The function performs these key setup tasks:
    1. Load environment variables from .env file
    2. Select and apply the appropriate configuration class
    3. Initialize URL configuration for different environments
    4. Configure secure session settings
    5. Validate required Auth0 environment variables
    6. Set up OAuth2 client with Auth0
    7. Register error handlers for common HTTP errors
    8. Register the authentication blueprint
    9. Create the home route

    Args:
        config_name (str): Configuration environment to use
            - 'development': Debug mode, localhost URLs, relaxed security
            - 'production': Secure settings, HTTPS required, no debug
            - 'testing': Test-friendly settings, CSRF disabled
            - 'default': Base configuration

    Returns:
        Flask: Fully configured Flask application instance ready to handle requests

    Raises:
        RuntimeError: If required Auth0 configuration variables are missing

    Example:
        # Create development app
        app = create_app('development')

        # Create production app
        app = create_app('production')
    """
    # Step 1: Load environment variables from .env file
    # This makes configuration available to the app before it starts
    load_dotenv(find_dotenv())

    # Step 2: Create Flask application instance
    app = Flask(__name__)

    # Step 3: Load configuration class based on environment
    # config is a dictionary mapping names to configuration classes
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
    # pylint: disable=import-outside-toplevel
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    app.logger.info("Application initialization completed")
    return app


def register_error_handlers(app):
    """
    Register HTTP error handlers for the Flask application.

    Registers custom error pages for common HTTP status codes:
    - 404: Page not found
    - 500: Internal server error
    - 403: Forbidden access

    Args:
        app (Flask): Flask application instance to register handlers on
    """

    @app.errorhandler(404)
    def not_found_error(_error):
        """Handle 404 Not Found errors."""
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        app.logger.error("Server Error: %s", error)
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden_error(_error):
        """Handle 403 Forbidden errors."""
        return render_template("errors/403.html"), 403

import os
from datetime import timedelta

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""

    # Flask settings
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    SECRET_KEY = os.getenv("APP_SECRET_KEY")

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SESSION_COOKIE_SECURE = FLASK_ENV == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Auth0 Configuration
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")

    # Validate required settings
    if not SECRET_KEY:
        if FLASK_ENV == "development":
            SECRET_KEY = "dev-secret-key-change-in-production"
        else:
            raise RuntimeError("APP_SECRET_KEY environment variable is not set.")

    # URL Configuration - Initialize as class variables
    _base_url = None

    @classmethod
    def init_urls(cls):
        """Initialize URL configuration."""
        if cls._base_url is None:
            cls._base_url = cls._get_base_url()
            cls.BASE_URL = cls._base_url
            cls.AUTH0_CALLBACK_URL = f"{cls._base_url}/auth/callback"
            cls.AUTH0_REDIRECT_URL = cls._base_url
            cls.AUTH0_BASE_URL = cls._base_url

    @staticmethod
    def _get_base_url():
        """Generate base URL based on environment."""
        codespace_name = os.getenv("CODESPACE_NAME")
        codespace_port = "5000"

        if codespace_name:
            return f"https://{codespace_name}-{codespace_port}.app.github.dev"
        else:
            return "http://localhost:5000"


class DevelopmentConfig(Config):
    """Development configuration."""

    FLASK_ENV = "development"
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration."""

    FLASK_ENV = "production"
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False


# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": Config,
}

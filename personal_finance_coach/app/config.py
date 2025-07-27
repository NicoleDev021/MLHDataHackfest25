# SPDX-FileCopyrightText: Copyright (c) 2025 Madison Nicole Goodwin https://github.com/NicoleDev021
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Application configuration classes for different environments.

This module provides configuration classes for:
- Base configuration with Auth0 and security settings
- Development configuration with debug mode
- Production configuration with security hardening
- Testing configuration for automated tests

Environment-specific URL generation for GitHub Codespaces and local development.
"""

import os
import secrets
from datetime import timedelta

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:  # pylint: disable=too-few-public-methods
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
            # Use a securely generated key for development
            # In production, this should always be set via environment variable
            SECRET_KEY = secrets.token_hex(32)  # Generate 64-character hex string
        else:
            raise RuntimeError("APP_SECRET_KEY environment variable is not set.")

    # URL Configuration - Initialize as class variables
    _base_url = None

    @classmethod
    def init_urls(cls):
        """
        Initialize URL configuration based on environment.

        This method is called once during app startup to configure URLs
        that Auth0 will use for callbacks and redirects.

        Why this is needed:
        - GitHub Codespaces generates dynamic URLs that we can't hardcode
        - Local development uses localhost:5000
        - Production might use a custom domain

        The method detects the environment and generates appropriate URLs:
        - CODESPACE_NAME environment variable indicates GitHub Codespaces
        - If CODESPACE_NAME exists, use the Codespaces URL format
        - Otherwise, default to localhost for local development

        URLs generated:
        - BASE_URL: Main application URL
        - AUTH0_CALLBACK_URL: Where Auth0 redirects after login
        - AUTH0_REDIRECT_URL: Where to go after logout
        - AUTH0_BASE_URL: Base URL for Auth0 configuration
        """
        if cls._base_url is None:
            # Generate base URL only once and cache it
            cls._base_url = cls._get_base_url()

            # Set all the URLs that Auth0 needs
            cls.BASE_URL = cls._base_url
            cls.AUTH0_CALLBACK_URL = f"{cls._base_url}/auth/callback"
            cls.AUTH0_REDIRECT_URL = cls._base_url
            cls.AUTH0_BASE_URL = cls._base_url

    @staticmethod
    def _get_base_url():
        """
        Generate base URL based on current environment.

        Automatically detects GitHub Codespaces environment and generates
        appropriate URLs, falling back to localhost for local development.

        Returns:
            str: Base URL for the application
        """
        codespace_name = os.getenv("CODESPACE_NAME")
        codespace_port = "5000"

        if codespace_name:
            return f"https://{codespace_name}-{codespace_port}.app.github.dev"
        return "http://localhost:5000"


class DevelopmentConfig(Config):  # pylint: disable=too-few-public-methods
    """
    Development configuration class.

    Extends base Config with development-specific settings:
    - Debug mode enabled
    - Less secure cookie settings for localhost
    - Development-friendly logging
    """

    FLASK_ENV = "development"
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):  # pylint: disable=too-few-public-methods
    """
    Production configuration class.

    Extends base Config with production-specific settings:
    - Debug mode disabled
    - Secure cookie settings enforced
    - Production logging levels
    - Enhanced security measures
    """

    FLASK_ENV = "production"
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):  # pylint: disable=too-few-public-methods
    """
    Testing configuration class.

    Extends base Config with testing-specific settings:
    - Testing mode enabled
    - CSRF protection disabled for easier testing
    - Less secure cookie settings for test environments
    - Isolated test database settings
    """

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

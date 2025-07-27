"""
Flask application entry point.

This module serves as the main entry point for the Personal Finance Coach application.
It handles:
- Environment-based configuration selection
- Application factory instantiation
- Development server startup with proper debug settings

Usage:
    python run.py

Environment Variables:
    FLASK_ENV: Application environment (development/production/testing)
    FLASK_DEBUG: Debug mode flag (true/false/1/0)

How it works:
1. Reads FLASK_ENV to determine which configuration to use
2. Calls create_app() factory function from app/__init__.py
3. Starts Flask development server on all interfaces (0.0.0.0) port 5000
4. Debug mode is enabled based on FLASK_DEBUG environment variable
"""

import os

from app import create_app

# Determine configuration based on environment
# This selects which Config class to use (Development, Production, etc.)
config_name = os.getenv("FLASK_ENV", "default")

# Create the Flask application using the factory pattern
# The create_app function is in app/__init__.py and handles all setup
app = create_app(config_name)

if __name__ == "__main__":
    # Only run the development server when this file is executed directly
    # In production, a WSGI server like Gunicorn would import 'app' instead

    # Check if debug mode should be enabled
    # Debug mode provides detailed error pages and auto-reloading
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() in ["1", "true"]

    # Start the Flask development server
    # host="0.0.0.0" makes it accessible from outside localhost (needed for Codespaces)
    # This is safe for development but should be changed to localhost in production
    # port=5000 is the default Flask port
    # debug=debug_mode enables/disables debug features
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)  # nosec B104

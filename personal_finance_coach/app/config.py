import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    SECRET_KEY = os.getenv("APP_SECRET_KEY")
    if not SECRET_KEY:
        if FLASK_ENV == "development":
            SECRET_KEY = "dev-secret-key"  # Fallback key for development only
        else:
            raise RuntimeError("APP_SECRET_KEY environment variable is not set.")
            
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    
    # Set URLs based on environment
    CODESPACE_NAME = os.getenv("CODESPACE_NAME")
    CODESPACE_PORT = "5000"  # Explicitly set port for Codespace
    
    if CODESPACE_NAME:
        # Force HTTPS and port 5000 for Codespace
        BASE_URL = f"https://{CODESPACE_NAME}-{CODESPACE_PORT}.app.github.dev"
        AUTH0_CALLBACK_URL = f"{BASE_URL}/auth/callback"
        # Add explicit port-specific redirect URL
        AUTH0_REDIRECT_URL = BASE_URL
    else:
        BASE_URL = "http://localhost:5000"
        AUTH0_CALLBACK_URL = f"{BASE_URL}/auth/callback"
        AUTH0_REDIRECT_URL = BASE_URL

    AUTH0_BASE_URL = BASE_URL
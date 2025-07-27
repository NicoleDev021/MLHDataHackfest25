import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("APP_SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("APP_SECRET_KEY environment variable is not set. The application cannot start without it.")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    
    # Set URLs based on environment
    CODESPACE_NAME = os.getenv("CODESPACE_NAME")
    if CODESPACE_NAME:
        AUTH0_CALLBACK_URL = f"https://{CODESPACE_NAME}-5000.app.github.dev/auth/callback"
        AUTH0_BASE_URL = f"https://{CODESPACE_NAME}-5000.app.github.dev"
        AUTH0_LOGIN_URL = f"https://{CODESPACE_NAME}-5000.app.github.dev/auth/login"
    else:
        AUTH0_CALLBACK_URL = "http://localhost:5000/auth/callback"
        AUTH0_BASE_URL = "http://localhost:5000"
        AUTH0_LOGIN_URL = "http://localhost:5000/auth/login"
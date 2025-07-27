import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "your-secret-key")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    
    # Determine the callback URL based on environment
    CODESPACE_NAME = os.getenv("CODESPACE_NAME")
    if CODESPACE_NAME:
        AUTH0_CALLBACK_URL = f"https://{CODESPACE_NAME}-5000.app.github.dev/callback"
    else:
        AUTH0_CALLBACK_URL = "http://localhost:5000/callback"
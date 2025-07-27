import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    if FLASK_ENV == 'development':
        SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    else:
        SECRET_KEY = os.environ.get('SECRET_KEY')
        if not SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable must be set in production.")
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
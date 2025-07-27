from flask import Flask, render_template, session, url_for, redirect, request
from authlib.integrations.flask_client import OAuth
from app.config import Config
import json
from urllib.parse import quote_plus, urlencode
import os
from dotenv import load_dotenv, find_dotenv

oauth = OAuth()

def create_app(config_class=Config):
    # Load environment variables from .env file
    load_dotenv(find_dotenv())

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = app.config["SECRET_KEY"]
    
    # Update base URL function to use environment variable
    def get_base_url():
        codespace_name = os.getenv('CODESPACE_NAME')
        if codespace_name:
            return f"https://{codespace_name}-5000.app.github.dev"
        return "http://localhost:5000"

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
            "token_endpoint_auth_method": "client_secret_post"
        },
    )

    # Add root route
    @app.route("/")
    def home():
        return render_template(
            "home.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )

    # Register the auth blueprint with correct import
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
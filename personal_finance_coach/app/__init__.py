from flask import Flask, render_template, session, url_for, redirect, request
from authlib.integrations.flask_client import OAuth
from app.config import Config
import json
from urllib.parse import quote_plus, urlencode
import os

oauth = OAuth()

def create_app(config_class=Config):
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
        },
    )

    # Update routes to use the correct base URL
    @app.route("/")
    def home():
        base_url = get_base_url()
        if not session.get("user"):
            return redirect(f"{base_url}/login")
        return render_template(
            "home.html",
            session=session.get("user"),
            pretty=json.dumps(session.get("user"), indent=4),
        )

    @app.route("/callback", methods=["GET", "POST"])
    def callback():
        try:
            token = oauth.auth0.authorize_access_token()
            session["user"] = token
            base_url = get_base_url()
            return redirect(f"{base_url}/")
        except Exception as e:
            app.logger.error(f"Callback error: {str(e)}")
            base_url = get_base_url()
            return redirect(f"{base_url}/login")

    @app.route("/login")
    def login():
        base_url = get_base_url()
        callback_url = f"{base_url}/callback"
        return oauth.auth0.authorize_redirect(redirect_uri=callback_url)

    @app.route("/logout")
    def logout():
        session.clear()
        base_url = get_base_url()
        return redirect(
            "https://"
            + app.config["AUTH0_DOMAIN"]
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": base_url,
                    "client_id": app.config["AUTH0_CLIENT_ID"],
                },
                quote_via=quote_plus,
            )
        )

    return app
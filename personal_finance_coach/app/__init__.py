from flask import Flask
from authlib.integrations.flask_client import OAuth
from app.config import Config

oauth = OAuth()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    oauth.init_app(app)
    oauth.register(
        'auth0',
        client_id=app.config['AUTH0_CLIENT_ID'],
        client_secret=app.config['AUTH0_CLIENT_SECRET'],
        api_base_url=f'https://{app.config["AUTH0_DOMAIN"]}',
        access_token_url=f'https://{app.config["AUTH0_DOMAIN"]}/oauth/token',
        authorize_url=f'https://{app.config["AUTH0_DOMAIN"]}/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    return app
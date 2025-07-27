from flask import Flask, redirect, url_for
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.auth.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
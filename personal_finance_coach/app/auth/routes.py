from flask import Blueprint, redirect, url_for, session
from app.auth.decorators import requires_auth
from app import oauth
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
    logger.debug("Login route called")
    try:
        return oauth.auth0.authorize_redirect(
            redirect_uri=url_for('auth.callback', _external=True)
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return f"Login error: {str(e)}", 500

@bp.route('/callback')
def callback():
    logger.debug("Callback route called")
    try:
        token = oauth.auth0.authorize_access_token()
        session['user'] = token
        return redirect(url_for('auth.dashboard'))
    except Exception as e:
        logger.error(f"Callback error: {str(e)}")
        return f"Callback error: {str(e)}", 500

@bp.route('/dashboard')
@requires_auth
def dashboard():
    return "Dashboard"
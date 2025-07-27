from flask import current_app as app, redirect, render_template, session, url_for
from app.auth import bp
from app import oauth
import logging
import json
from urllib.parse import urlencode, quote_plus

logger = logging.getLogger(__name__)

@bp.route('/login')
def login():
    logger.debug("Login route called")
    return oauth.auth0.authorize_redirect(
        redirect_uri=app.config['AUTH0_CALLBACK_URL']
    )

@bp.route('/callback')
def callback():
    logger.debug("Callback route called")
    try:
        token = oauth.auth0.authorize_access_token()
        userinfo = token.get('userinfo')
        if not userinfo:
            logger.error("No userinfo in token")
            return redirect(url_for('auth.login'))

        session['user'] = token
        session['profile'] = {
            'name': userinfo.get('name'),
            'email': userinfo.get('email'),
            'picture': userinfo.get('picture')
        }
        
        logger.debug(f"User authenticated: {session['profile'].get('email')}")
        
        # Use explicit port URL for redirect
        redirect_url = f"{app.config['AUTH0_REDIRECT_URL']}/auth/dashboard"
        logger.debug(f"Redirecting to: {redirect_url}")
        return redirect(redirect_url)
    except Exception as e:
        logger.error(f"Callback error: {str(e)}")
        return redirect(url_for('auth.login'))

@bp.route('/dashboard')
def dashboard():
    if not session.get('profile'):
        logger.debug("No profile in session, redirecting to login")
        return redirect(url_for('auth.login'))
        
    profile = session.get('profile', {})
    userinfo = {
        'name': profile.get('name'),
        'email': profile.get('email'),
        'picture': profile.get('picture')
    }
    
    logger.debug(f"Loading dashboard for user: {userinfo.get('email')}")
    return render_template(
        'auth/dashboard.html',  # Make sure this path matches your template location
        userinfo=userinfo,
        pretty=json.dumps(userinfo, indent=4)
    )

@bp.route('/logout')
def logout():
    session.clear()
    base_url = app.config['BASE_URL']
    
    logger.debug(f"Logging out. Redirect URL: {base_url}")
    
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
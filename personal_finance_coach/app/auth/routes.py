from flask import current_app as app
from flask import redirect, render_template, session, url_for
from app.auth import bp
from app.auth.decorators import login_required
from urllib.parse import urlencode

@bp.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=app.config['AUTH0_CALLBACK_URL']
    )

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
    return render_template('auth/dashboard.html',
                         userinfo=session['profile'])

@bp.route('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for('auth.login', _external=True),
        'client_id': app.config['AUTH0_CLIENT_ID']
    }
    return redirect(oauth.auth0.api_base_url + '/v2/logout?' + urlencode(params))
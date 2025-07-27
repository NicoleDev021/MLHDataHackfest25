from flask import current_app as app
from flask import redirect, render_template, session, url_for
from app.auth import bp
from app.auth.decorators import requires_auth
from urllib.parse import urlencode

@bp.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=app.config.get('AUTH0_CALLBACK_URL', 'http://localhost:5000/callback')
    )

@bp.route('/callback')
def callback():
    oauth.auth0.authorize_access_token()
    resp = oauth.auth0.get('userinfo')
    userinfo = resp.json()
    
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo.get('name', ''),
        'email': userinfo.get('email', ''),
        'picture': userinfo.get('picture', '')
    }
    
    return redirect(url_for('auth.dashboard'))

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
    return redirect(f"https://{app.config['AUTH0_DOMAIN']}/v2/logout?" + urlencode(params))
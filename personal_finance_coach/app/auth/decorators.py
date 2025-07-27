from functools import wraps
from flask import session, redirect, url_for

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated
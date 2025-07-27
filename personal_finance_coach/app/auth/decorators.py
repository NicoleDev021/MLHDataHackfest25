"""Authentication decorators for the application."""

import logging
from functools import wraps

from flask import flash, redirect, session, url_for

logger = logging.getLogger(__name__)


def requires_auth(f):
    """
    Decorator that requires user authentication.

    Redirects to login if user is not authenticated.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "profile" not in session:
            logger.debug(f"Unauthorized access attempt to {f.__name__}")
            flash("Please log in to access this page.", "info")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def requires_role(role):
    """
    Decorator that requires a specific user role.

    Args:
        role (str): Required role for access
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "profile" not in session:
                logger.debug(f"Unauthorized access attempt to {f.__name__}")
                flash("Please log in to access this page.", "info")
                return redirect(url_for("auth.login"))

            user_roles = session.get("profile", {}).get("roles", [])
            if role not in user_roles:
                logger.warning(
                    f"Insufficient permissions for {f.__name__}: required {role}"
                )
                flash("You don't have permission to access this page.", "error")
                return redirect(url_for("home"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator

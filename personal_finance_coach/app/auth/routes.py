import json
import logging
from urllib.parse import quote_plus, urlencode

from flask import current_app as app
from flask import flash, redirect, render_template, session, url_for

from app import oauth
from app.auth import bp
from app.validation import validate_user_profile

logger = logging.getLogger(__name__)


@bp.route("/login")
def login():
    """Initiate Auth0 login process."""
    logger.debug("Login route called")
    try:
        return oauth.auth0.authorize_redirect(
            redirect_uri=app.config["AUTH0_CALLBACK_URL"]
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        flash("Login service temporarily unavailable. Please try again.", "error")
        return redirect(url_for("home"))


@bp.route("/callback")
def callback():
    """Handle Auth0 callback after authentication."""
    logger.debug("Callback route called")
    try:
        # Get token from Auth0
        token = oauth.auth0.authorize_access_token()
        if not token:
            logger.error("No token received from Auth0")
            flash("Authentication failed. Please try again.", "error")
            return redirect(url_for("auth.login"))

        # Extract user info
        userinfo = token.get("userinfo")
        if not userinfo:
            logger.error("No userinfo in token")
            flash("Failed to retrieve user information.", "error")
            return redirect(url_for("auth.login"))

        # Validate user profile data
        profile_data = {
            "name": userinfo.get("name", "Unknown User"),
            "email": userinfo.get("email", ""),
            "picture": userinfo.get("picture"),
        }

        logger.debug(f"Raw userinfo from Auth0: {userinfo}")
        logger.debug(f"Processed profile data: {profile_data}")

        # Try validation, but be lenient with failures
        validated_profile, validation_error = validate_user_profile(profile_data)
        if validation_error:
            logger.warning(f"Profile validation warning: {validation_error}")
            # Use the original data with some cleanup instead of failing
            validated_profile = {
                "name": profile_data.get("name", "Unknown User"),
                "email": profile_data.get("email") if profile_data.get("email") else None,
                "picture": profile_data.get("picture") if profile_data.get("picture") else None,
            }
            logger.info("Using cleaned profile data despite validation warnings")

        # Store user data in session
        session["user"] = token
        session["profile"] = validated_profile
        session.permanent = True

        user_identifier = validated_profile.get('email') or validated_profile.get('name') or 'Unknown'
        logger.info(f"User authenticated successfully: {user_identifier}")

        # Redirect to dashboard
        return redirect(url_for("auth.dashboard"))

    except Exception as e:
        logger.error(f"Callback error: {str(e)}")
        flash("Authentication failed. Please try again.", "error")
        return redirect(url_for("auth.login"))


@bp.route("/dashboard")
def dashboard():
    """User dashboard - requires authentication."""
    profile = session.get("profile")
    if not profile:
        logger.debug("No profile in session, redirecting to login")
        flash("Please log in to access your dashboard.", "info")
        return redirect(url_for("auth.login"))

    # Sanitize user info for display
    userinfo = {
        "name": profile.get("name", "Unknown"),
        "email": profile.get("email", ""),
        "picture": profile.get("picture", ""),
    }

    logger.debug(f"Loading dashboard for user: {userinfo['email']}")
    return render_template(
        "auth/dashboard.html",
        userinfo=userinfo,
        pretty=json.dumps(userinfo, indent=4),
    )


@bp.route("/debug")
def debug():
    """Debug route to check session data."""
    if not session.get("profile"):
        return {"error": "No profile in session", "session_keys": list(session.keys())}
    
    return {
        "profile": session.get("profile"),
        "user_keys": list(session.get("user", {}).keys()) if session.get("user") else [],
        "session_keys": list(session.keys())
    }


@bp.route("/logout")
def logout():
    """Log out user and clear session."""
    email = session.get("profile", {}).get("email", "unknown")
    logger.info(f"User logging out: {email}")

    session.clear()

    # Construct Auth0 logout URL
    logout_url = f"https://{app.config['AUTH0_DOMAIN']}/v2/logout?" + urlencode(
        {
            "returnTo": app.config["BASE_URL"],
            "client_id": app.config["AUTH0_CLIENT_ID"],
        },
        quote_via=quote_plus,
    )

    flash("You have been logged out successfully.", "success")
    return redirect(logout_url)

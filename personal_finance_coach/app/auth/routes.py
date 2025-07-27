"""
Authentication routes for Auth0 integration.

This module handles all authentication-related routes including:
- OAuth2 login initiation with Auth0
- Auth0 callback processing and token validation
- User session management and profile storage
- Protected dashboard access
- Secure logout with Auth0 session termination
- Debug utilities for development

All routes include comprehensive error handling and logging.
"""

# pylint: disable=cyclic-import

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
    except (KeyError, AttributeError, ValueError) as e:
        logger.error("Login configuration error: %s", str(e))
        flash("Login service temporarily unavailable. Please try again.", "error")
        return redirect(url_for("home"))
    except (ConnectionError, TimeoutError) as e:
        logger.error("Auth0 connection error: %s", str(e))
        flash("Login service temporarily unavailable. Please try again.", "error")
        return redirect(url_for("home"))


@bp.route("/callback")
def callback():
    """
    Handle Auth0 callback after authentication.

    This is the most complex route in the application. Here's what happens:

    1. User completes login on Auth0 and is redirected here with authorization code
    2. We exchange the authorization code for an access token
    3. We extract user profile information from the token
    4. We validate and clean the user data
    5. We store user information in the Flask session
    6. We redirect user to their dashboard

    Error handling covers:
    - Missing or invalid tokens from Auth0
    - Missing user information in token
    - Data validation failures
    - Any unexpected exceptions during the process
    """
    logger.debug("Callback route called")
    try:
        # Step 1: Exchange authorization code for access token
        # This communicates with Auth0's token endpoint securely
        token = oauth.auth0.authorize_access_token()
        if not token:
            logger.error("No token received from Auth0")
            flash("Authentication failed. Please try again.", "error")
            return redirect(url_for("auth.login"))

        # Step 2: Extract user information from the token
        # The token contains user profile data from Auth0
        userinfo = token.get("userinfo")
        if not userinfo:
            logger.error("No userinfo in token")
            flash("Failed to retrieve user information.", "error")
            return redirect(url_for("auth.login"))

        # Step 3: Prepare user profile data for validation
        # We extract only the fields we need and provide defaults
        profile_data = {
            "name": userinfo.get("name", "Unknown User"),
            "email": userinfo.get("email", ""),
            "picture": userinfo.get("picture"),
        }

        logger.debug("Raw userinfo from Auth0: %s", userinfo)
        logger.debug("Processed profile data: %s", profile_data)

        # Step 4: Validate user profile data using Marshmallow schema
        # This ensures data integrity and handles missing/invalid fields
        validated_profile, validation_error = validate_user_profile(profile_data)
        if validation_error:
            logger.warning("Profile validation warning: %s", validation_error)
            # Use the original data with some cleanup instead of failing
            # This makes the auth process more resilient to data variations
            validated_profile = {
                "name": profile_data.get("name", "Unknown User"),
                "email": (
                    profile_data.get("email") if profile_data.get("email") else None
                ),
                "picture": (
                    profile_data.get("picture") if profile_data.get("picture") else None
                ),
            }
            logger.info("Using cleaned profile data despite validation warnings")

        # Step 5: Store user data in Flask session
        # Session data is encrypted and stored in secure cookies
        session["user"] = token  # Store full OAuth token for API calls if needed
        session["profile"] = validated_profile  # Store cleaned profile data
        session.permanent = True  # Enable session timeout (set in config)

        # Log successful authentication (using email or name as identifier)
        user_identifier = (
            validated_profile.get("email") or validated_profile.get("name") or "Unknown"
        )
        logger.info("User authenticated successfully: %s", user_identifier)

        # Step 6: Redirect to dashboard
        # User is now fully authenticated and can access protected routes
        return redirect(url_for("auth.dashboard"))

    except (KeyError, AttributeError, TypeError, ValueError) as e:
        logger.error("Auth0 callback data error: %s", str(e))
        flash("Authentication failed. Please try again.", "error")
        return redirect(url_for("auth.login"))
    except (ConnectionError, TimeoutError) as e:
        logger.error("Auth0 callback connection error: %s", str(e))
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

    logger.debug("Loading dashboard for user: %s", userinfo["email"])
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
        "user_keys": (
            list(session.get("user", {}).keys()) if session.get("user") else []
        ),
        "session_keys": list(session.keys()),
    }


@bp.route("/logout")
def logout():
    """Log out user and clear session."""
    email = session.get("profile", {}).get("email", "unknown")
    logger.info("User logging out: %s", email)

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

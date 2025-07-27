"""Validation schemas for the application."""

from marshmallow import Schema, fields, validate


class UserProfileSchema(Schema):
    """Schema for validating user profile data."""

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Name is required"},
    )
    email = fields.Email(
        required=False,  # Make email optional since Auth0 might not always provide it
        allow_none=True,
        dump_default=None,
        load_default=None,
        error_messages={
            "required": "Email is required",
            "invalid": "Invalid email format",
        },
    )
    picture = fields.Url(
        allow_none=True, 
        required=False,
        dump_default=None,
        load_default=None,
        error_messages={"invalid": "Invalid URL format"}
    )


class AuthTokenSchema(Schema):
    """Schema for validating Auth0 tokens."""

    access_token = fields.Str(required=True)
    id_token = fields.Str(required=True)
    userinfo = fields.Dict(required=True)
    expires_at = fields.Int(allow_none=True)


def validate_user_profile(profile_data):
    """Validate user profile data."""
    import logging
    logger = logging.getLogger(__name__)
    
    # Log the incoming data for debugging
    logger.debug(f"Validating profile data: {profile_data}")
    
    schema = UserProfileSchema()
    try:
        result = schema.load(profile_data)
        logger.debug(f"Validation successful: {result}")
        return result, None
    except Exception as e:
        logger.error(f"Validation failed for data {profile_data}: {str(e)}")
        return None, str(e)


def validate_auth_token(token_data):
    """Validate Auth0 token data."""
    schema = AuthTokenSchema()
    try:
        result = schema.load(token_data)
        return result, None
    except Exception as e:
        return None, str(e)

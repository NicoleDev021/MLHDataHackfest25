# SPDX-FileCopyrightText: Copyright (c) 2025 Madison Nicole Goodwin https://github.com/NicoleDev021
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Data validation schemas for the Personal Finance Coach application.

This module uses Marshmallow to validate and sanitize data from external sources
(primarily Auth0 user profiles). Validation ensures data integrity and security.

Why we validate data:
- Auth0 might send unexpected or missing fields
- User input could be malicious or malformed
- Different Auth0 configurations return different data structures
- We want consistent data format throughout our application

Marshmallow features used:
- Schema classes define expected data structure
- Field types provide automatic validation (email, URL, string length)
- Custom error messages for user-friendly feedback
- Graceful handling of missing or invalid data
"""

import logging
from marshmallow import Schema, fields, validate, ValidationError


class UserProfileSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for validating user profile data from Auth0.

    This schema validates the user profile information we receive from Auth0
    after successful authentication. It ensures we have clean, consistent
    data to store in the user's session.

    Fields:
    - name: User's display name (required, 1-100 characters)
    - email: User's email address (optional, must be valid email format)
    - picture: URL to user's profile picture (optional, must be valid URL)

    Why email is optional:
    - Some Auth0 configurations don't require email verification
    - Social logins might not provide email access
    - We don't want authentication to fail just because email is missing
    """

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
        error_messages={"invalid": "Invalid URL format"},
    )


class AuthTokenSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Schema for validating Auth0 OAuth2 tokens.

    This schema validates the complete token response from Auth0,
    ensuring all required components are present for the OAuth2 flow.

    Fields:
    - access_token: Token for API access (required)
    - id_token: JWT with user identity information (required)
    - userinfo: User profile information (required)
    - expires_at: Token expiration timestamp (optional)
    """

    access_token = fields.Str(required=True)
    id_token = fields.Str(required=True)
    userinfo = fields.Dict(required=True)
    expires_at = fields.Int(allow_none=True)


def validate_user_profile(profile_data):
    """
    Validate user profile data using UserProfileSchema.

    This function is called during the Auth0 callback process to ensure
    the user profile data is clean and safe to store in the session.

    Args:
        profile_data (dict): Raw user profile data from Auth0

    Returns:
        tuple: (validated_data, error_message)
        - If successful: (dict with validated data, None)
        - If failed: (None, error message string)

    Example:
        profile_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'picture': 'https://example.com/avatar.jpg'
        }

        validated_profile, error = validate_user_profile(profile_data)
        if error:
            print(f"Validation failed: {error}")
        else:
            print(f"Validated data: {validated_profile}")
    """
    logger = logging.getLogger(__name__)

    # Log the incoming data for debugging (helps with Auth0 integration issues)
    logger.debug("Validating profile data: %s", profile_data)

    schema = UserProfileSchema()
    try:
        # load() validates and returns clean data
        result = schema.load(profile_data)
        logger.debug("Validation successful: %s", result)
        return result, None
    except ValidationError as e:
        # Handle Marshmallow validation errors specifically
        logger.error("Validation failed for data %s: %s", profile_data, str(e))
        return None, str(e)
    except (TypeError, AttributeError, KeyError) as e:
        # Handle data structure errors
        logger.error("Data structure error for %s: %s", profile_data, str(e))
        return None, str(e)
    except (ValueError, OSError) as e:
        # Handle common validation/data errors that could occur during processing
        logger.error("Data processing error for data %s: %s", profile_data, str(e))
        return None, str(e)


def validate_auth_token(token_data):
    """
    Validate Auth0 token data using AuthTokenSchema.

    This function ensures the OAuth2 token response from Auth0
    contains all required fields for proper authentication.

    Args:
        token_data (dict): Raw token response from Auth0

    Returns:
        tuple: (validated_data, error_message)
        - If successful: (dict with validated data, None)
        - If failed: (None, error message string)
    """
    schema = AuthTokenSchema()
    try:
        result = schema.load(token_data)
        return result, None
    except ValidationError as e:
        return None, str(e)
    except (TypeError, AttributeError, KeyError) as e:
        return None, str(e)
    except (ValueError, OSError) as e:
        return None, str(e)

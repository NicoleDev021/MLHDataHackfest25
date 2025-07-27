# SPDX-FileCopyrightText: Copyright (c) 2025 Madison Nicole Goodwin https://github.com/NicoleDev021
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Authentication blueprint module.

This module initializes the authentication blueprint and imports
authentication routes for Auth0 integration including:
- Login/logout functionality
- OAuth2 callback handling
- Protected route decorators
- User session management
"""

from flask import Blueprint

bp = Blueprint("auth", __name__)

# Import routes after blueprint creation to avoid circular imports
# pylint: disable=wrong-import-position,unused-import
from app.auth import routes  # noqa: E402,F401

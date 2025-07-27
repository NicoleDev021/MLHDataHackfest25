# SPDX-FileCopyrightText: Copyright (c) 2025 Madison Nicole Goodwin https://github.com/NicoleDev021
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Logging configuration for the application."""

import logging
import logging.config
import os
from datetime import datetime


def setup_logging(app):
    """Configure logging for the application."""

    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(app.instance_path), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Log file names
    error_log = os.path.join(logs_dir, "error.log")
    access_log = os.path.join(logs_dir, "access.log")

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": (
                    "[%(asctime)s] %(levelname)s in %(module)s "
                    "[%(pathname)s:%(lineno)d]: %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": error_log,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "default",
                "filename": access_log,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "app": {
                "level": "DEBUG" if app.config.get("DEBUG") else "INFO",
                "handlers": ["console", "error_file", "access_file"],
                "propagate": False,
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }

    logging.config.dictConfig(logging_config)

    # Set Flask's logger
    app_logger = logging.getLogger("app")
    app.logger.handlers.clear()

    # Only add handlers if they exist
    if app_logger.handlers:
        for handler in app_logger.handlers:
            app.logger.addHandler(handler)

    app.logger.setLevel(logging.DEBUG if app.config.get("DEBUG") else logging.INFO)

    app.logger.info(f"Application started at {datetime.now()}")

    return app_logger

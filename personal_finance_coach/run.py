import os

from app import create_app

# Determine configuration based on environment
config_name = os.getenv("FLASK_ENV", "default")
app = create_app(config_name)

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() in ["1", "true"]
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)

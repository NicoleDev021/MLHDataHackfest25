import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() in ['1', 'true']
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug_mode
    )
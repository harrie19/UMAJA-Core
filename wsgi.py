"""
WSGI Production Entrypoint for UMAJA-Core
Exposes the Flask application for WSGI servers (gunicorn, uWSGI, etc.)

Supports both World Tour and Beta System:
- Set BETA_MODE=true to use beta_server
- Default: simple_server (World Tour)
"""

import os

# Choose server based on environment variable
BETA_MODE = os.environ.get('BETA_MODE', 'false').lower() == 'true'

if BETA_MODE:
    from api.beta_server import app
    print("🐰 UMAJA Beta System loaded")
else:
    from api.simple_server import app
    print("🌍 UMAJA World Tour System loaded")

# Expose both 'app' and 'application' for different WSGI servers
application = app

if __name__ == "__main__":
    # Development mode only - do not use in production
    # In production, use: gunicorn --bind 0.0.0.0:$PORT wsgi:app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

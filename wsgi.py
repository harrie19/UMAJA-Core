"""
WSGI Production Entrypoint for UMAJA-Core
Exposes the Flask application for WSGI servers (gunicorn, uWSGI, etc.)
"""

from api.simple_server import app

# Expose both 'app' and 'application' for different WSGI servers
application = app

if __name__ == "__main__":
    # Development mode only - do not use in production
    # In production, use: gunicorn --bind 0.0.0.0:$PORT wsgi:app
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

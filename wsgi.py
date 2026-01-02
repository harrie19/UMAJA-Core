"""
WSGI Production Entrypoint for UMAJA-Core
Exposes the Flask application for WSGI servers (gunicorn, uWSGI, etc.)
"""

from api.simple_server import app

# Expose both 'app' and 'application' for different WSGI servers
application = app

if __name__ == "__main__":
    # Development server fallback
    app.run()

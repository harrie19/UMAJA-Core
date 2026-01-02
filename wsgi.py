"""
WSGI entry point for production deployment
"""
from api.simple_server import app

# For WSGI servers like Gunicorn
application = app

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

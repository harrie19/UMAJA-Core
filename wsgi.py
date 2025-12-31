"""WSGI entrypoint for UMAJA-Core."""

from api.simple_server import app

# Alias for servers that look for `application`
application = app

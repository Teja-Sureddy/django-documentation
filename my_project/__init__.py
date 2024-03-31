"""
ASGI (Asynchronous Server Gateway Interface):
It is a protocol used for asynchronous operations and WebSockets.
ASGI servers like Daphne or Uvicorn, handle the asynchronous requests and communicate with Django applications via ASGI protocol.


WSGI (Web Server Gateway Interface):
It is an interface between the Django app and the web server.
WSGI servers like Gunicorn or uWSGI, handle incoming HTTP requests, pass them to the Django app through WSGI, and return responses to the clients.
"""
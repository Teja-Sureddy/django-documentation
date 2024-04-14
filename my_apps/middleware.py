"""
A pipeline is a series of middlewares that process a request and response in a sequential manner.

Middleware allows you to alter the processing of requests and responses.
"""

from rest_framework.authentication import TokenAuthentication
import json
from my_apps.users.models import AuditLog
from django.urls import reverse


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if not user:
            try:
                user, token = TokenAuthentication().authenticate(request)
            except Exception:
                pass

        # audit
        user = user if user.id else None
        method = request.method
        path = request.path
        params = json.dumps(dict(request.GET))

        if self.is_valid_path(path):
            obj = {"user": user, "method": method, "path": path, "params": params}
            AuditLog.objects.create(**obj)

        response = self.get_response(request)
        return response

    @staticmethod
    def is_valid_path(path: str):
        is_valid = True

        ignored_names = ["home_redirect", "login_redirect"]
        for name in ignored_names:
            if path == reverse(name):
                is_valid = False
                break

        if "__debug__" in path:
            is_valid = False

        return is_valid


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Informs browsers that the site should only be accessed using HTTPS for a specified period of time.
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # It prevents MIME-sniffing attacks.
        response["X-Content-Type-Options"] = "nosniff"

        # It prevents a web page from being displayed within an iframe, embed, ...
        response["X-Frame-Options"] = "DENY"

        # It helps detect and block certain types of XSS attacks.
        response["X-XSS-Protection"] = "1; mode=block"

        # It controls how much referrer information should be included with requests.
        response["Referrer-Policy"] = "same-origin"

        # Web developers can explicitly declare what functionality can and cannot be used on a website.
        response["Feature-Policy"] = (
            "camera 'self'; microphone 'self'; fullscreen 'self' 'allowfullscreen'"
        )
        response["Permissions-Policy"] = (
            "camera=(self), microphone=(self), geolocation=(), accelerometer=(), "
            "gyroscope=(), magnetometer=(), payment=(), fullscreen=(self)"
        )

        return response

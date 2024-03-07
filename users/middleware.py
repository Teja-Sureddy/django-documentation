from rest_framework.authentication import TokenAuthentication
import json
from users.models import AuditLog
from django.urls import reverse


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if not user:
            try:
                user, token = TokenAuthentication().authenticate(request)
            except:
                pass

        # audit
        user = user if user.id else None
        method = request.method
        path = request.path
        headers = json.dumps(dict(request.headers))
        params = json.dumps(dict(request.GET))
        body = json.dumps(request.body.decode('utf-8'))

        if self.is_valid_path(path):
            obj = {'user': user, 'method': method, 'path': path, 'headers': headers, 'params': params, 'body': body}
            AuditLog.objects.create(**obj)

        response = self.get_response(request)
        return response

    @staticmethod
    def is_valid_path(path: str):
        is_valid = True

        ignored_names = ['home_redirect', 'login_redirect']
        for name in ignored_names:
            if path == reverse(name):
                is_valid = False
                break

        if '__debug__' in path:
            is_valid = False

        return is_valid

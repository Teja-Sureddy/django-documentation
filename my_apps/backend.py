"""
Backends typically run when Django initializes or when specific operations related to their functionality are triggered within the application.
For example,
authentication backends are called when a user tries to authenticate,
database backends are involved when database operations are performed, and so on.
"""
from allauth.account.auth_backends import AuthenticationBackend


class MyCustomAuthBackend(AuthenticationBackend):
    def authenticate(self, request, **credentials):
        super().authenticate(request, **credentials)

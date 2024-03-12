from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, BasicAuthentication


# For basic authentication, you include the username and password in the request headers for every request.
# This is bad as it involves sending sensitive information with every request.
class BasicAuthenticationView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Authenticated as user: {}'.format(request.user)}
        return Response(content)


# With session authentication, you typically log in once by sending a request to a login endpoint with your credentials.
# Once you're authenticated, the server sets a session cookie in your browser.
class SessionAuthenticationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Authenticated as user: {}'.format(request.user)}
        return Response(content)


# You typically obtain a token by sending a request to a token endpoint with your credentials.
# Once you have the token, you include it in the request headers for subsequent API requests.
class TokenAuthenticationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Authenticated as user: {}'.format(request.user)}
        return Response(content)

from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.views import LoginView, LogoutView
from my_apps.rest.views import BasicAuthenticationView, SessionAuthenticationView, TokenAuthenticationView

app_name = "rest_framework"
urlpatterns = [
    # basic auth
    path('verify/basic/', BasicAuthenticationView.as_view(), name='basic'),
    # session auth
    path('auth/login/', LoginView.as_view(template_name='rest_framework/login.html'), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('verify/session/', SessionAuthenticationView.as_view(), name='session'),
    # token auth
    path('auth/token/', ObtainAuthToken.as_view(), name='auth-token'),
    path('verify/token/', TokenAuthenticationView.as_view(), name='token'),
]

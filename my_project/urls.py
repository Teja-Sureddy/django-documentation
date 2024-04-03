"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
# auth
from allauth.account import views
# social auth
from allauth.socialaccount.providers.google.views import login_by_token
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.socialaccount.providers.google.provider import GoogleProvider


# all-auth authentication
auth_urlpatterns = [
    path("", RedirectView.as_view(url='login/'), name='login_redirect'),
    path("login/", views.login, name="account_login"),
    path("signup/", views.signup, name="account_signup"),
    path("logout/", views.logout, name="account_logout"),

    # password reset
    path("password/reset/", views.password_reset, name="account_reset_password"),
    path("password/reset/done/", views.password_reset_done, name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", views.password_reset_from_key,
            name="account_reset_password_from_key"),
    path("password/reset/key/done/", views.password_reset_from_key_done, name="account_reset_password_from_key_done"),

    # Email
    path("confirm-email/", views.email_verification_sent, name="account_email_verification_sent"),
    re_path(r"^confirm-email/(?P<key>[-:\w]+)/$", views.confirm_email, name="account_confirm_email"),
]

# all-auth social authentication
social_auth_urlpatterns = \
    [
        # Google
        path("google/login/token/", login_by_token, name="google_login_by_token"),
    ] + default_urlpatterns(GoogleProvider)

# mfa authentication
mfa_urlpatterns = [
    path("reauthenticate/", views.reauthenticate, name="account_reauthenticate"),
    path("2fa/", include("allauth.mfa.urls"))
]

urlpatterns = [
    path('', RedirectView.as_view(url='/user/'), name='home_redirect'),
    path('', include('my_apps.users.urls')),
    path('user/', include(auth_urlpatterns + social_auth_urlpatterns + mfa_urlpatterns)),
    path('dashboard/', include('my_apps.dashboard.urls')),
    path('api/', include('my_apps.rest.urls')),
    path('notification/', include('my_apps.notification.urls')),
    path('background/', include('my_apps.background_task.urls')),
    path('pdf/', include('my_apps.pdf.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
]

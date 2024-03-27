from django.urls import path, include, re_path
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.views import LoginView, LogoutView
from my_apps.rest.views import *
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns


# Viewset
router = SimpleRouter()
router.register('class_viewset', ClassViewset, basename='class_viewset'),


app_name = "rest_framework"
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include([
        # basic auth
        path('verify/basic/', BasicAuthenticationView.as_view(), name='basic'),
        # session auth
        path('auth/login/', LoginView.as_view(template_name='rest_framework/login.html'), name='login'),
        path('auth/logout/', LogoutView.as_view(), name='logout'),
        path('verify/session/', SessionAuthenticationView.as_view(), name='session'),
        # token auth
        path('auth/token/', ObtainAuthToken.as_view(), name='auth-token'),
        path('verify/token/', TokenAuthenticationView.as_view(), name='token'),
    ]))
]


urlpatterns = urlpatterns + [
    path('v1/', include(
        format_suffix_patterns([
            # Function based
            path('function_api_view/', function_api_view, name='function_api_view'),
            path('function_api_view/<int:pk>/', function_api_pk_view, name='function_api_pk_view'),
            # Class based
            path('class_api_view/', ClassApiView.as_view(), name='class_api_view'),
            path('class_api_view/<int:pk>/', ClassApiPkView.as_view(), name='class_api_pk_view'),
            # Generic
            path('class_generic_view/', ClassGenericsView.as_view(), name='class_generic_view'),
            path('class_generic_view/<int:pk>/', ClassGenericsPkView.as_view(), name='class_generic_pk_view'),
        ])
    ))]

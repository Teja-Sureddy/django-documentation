from django.urls import path
from users.views import LoginView


app_name = "users"
urlpatterns = [
    path("", LoginView.as_view(), name="login")
]

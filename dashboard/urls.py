from django.urls import path
from dashboard.views import ProfileView


app_name = "dashboard"
urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
]

from django.urls import path
from dashboard.views import ProfileView, ProfileModifyView


app_name = "dashboard"
urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/add/", ProfileModifyView.as_view(), name="profile-add"),
    path("profile/edit/<pk>/", ProfileModifyView.as_view(), name="profile-edit"),
    path("profile/delete/<int:pk>/", ProfileView.as_view(), name="profile-delete"),
]

from django.urls import path
from dashboard.views import ProfileView, ProfileAddView


app_name = "dashboard"
urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/add/", ProfileAddView.as_view(), name="profile-add"),
    path("profile/edit/<int:pk>/", ProfileView.as_view(), name="profile-edit"),
    path("profile/delete/<int:pk>/", ProfileView.as_view(), name="profile-delete"),
]

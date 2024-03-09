from django.urls import path
from users.views import ProfileView, AccessFileView
from django.contrib.auth.decorators import login_required


app_name = "users"
urlpatterns = [
    path("profile/", login_required(ProfileView.as_view()), name="profile"),
    path('assets/public/<str:filename>/', AccessFileView.as_view(), name='access_file'),
    path('assets/<str:directory>/<int:user_id>/<str:filename>/', login_required(AccessFileView.as_view()), name='access_file'),
]

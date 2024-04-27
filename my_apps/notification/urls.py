from django.urls import path
from my_apps.notification.views import notification_read_view
from django.contrib.auth.decorators import login_required

app_name = "notification"

urlpatterns = [
    path(
        "mark-as-read/<int:slug>/",
        login_required(notification_read_view),
        name="notification_read",
    ),
]

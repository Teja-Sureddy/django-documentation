from django.urls import re_path
from my_apps.notification.consumers import NotificationConsumer
from my_apps.notification.views import notification_read_view
from django.contrib.auth.decorators import login_required

app_name = "notification"

websocket_urlpatterns = [
    re_path('ws/notification/$', NotificationConsumer.as_asgi()),
]

urlpatterns = [
    re_path(r'^mark-as-read/(?P<slug>\d+)/$', login_required(notification_read_view), name='notification_read'),
]

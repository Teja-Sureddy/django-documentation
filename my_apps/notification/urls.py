from django.urls import re_path
from my_apps.notification.consumers import NotificationConsumer

app_name = "notification"

websocket_urlpatterns = [
    re_path('ws/notification/$', NotificationConsumer.as_asgi()),
]

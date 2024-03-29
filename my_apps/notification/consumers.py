from channels.generic.websocket import AsyncJsonWebsocketConsumer
from notifications.models import Notification
from asgiref.sync import sync_to_async
from my_apps.notification.signals import notify_instance_to_data
from django.db.models import Q


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    common_channel = 'notification'
    user_channel = None

    async def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            self.user_channel = f"user_{user.id}"
            await self.channel_layer.group_add(self.user_channel, self.channel_name)

        await self.channel_layer.group_add(self.common_channel, self.channel_name)
        await self.accept()
        await self.send_existing_notifications(user)

    async def disconnect(self, code):
        if hasattr(self, 'user_channel') and self.user_channel:
            await self.channel_layer.group_discard(self.user_channel, self.channel_name)

        await self.channel_layer.group_discard(self.common_channel, self.channel_name)

    async def notify_message(self, event):
        # Send message to WebSocket
        await self.send_json(event['message'])

    async def send_existing_notifications(self, user):
        """
        Custom method to send the existing data.
        """
        if user.is_authenticated:
            queryset = await sync_to_async(Notification.objects.filter)(Q(public=True) | Q(recipient=user))
        else:
            queryset = await sync_to_async(Notification.objects.filter)(public=True)

        queryset = await sync_to_async(queryset.order_by)('-timestamp')
        queryset = queryset[:10]

        notifications = await sync_to_async(list)(queryset)
        for instance in reversed(notifications):
            await self.send_json(notify_instance_to_data(instance))

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import Notification
from django.utils.timesince import timesince


@receiver(post_save, sender=Notification)
def create_notification(sender, instance, created, **kwargs):
    common_channel = 'notification'
    send_to_wss_def_name = 'notify_message'

    if created:
        data = notify_instance_to_data(instance)
        event = {'type': send_to_wss_def_name, 'message': data}
        channel_layer = get_channel_layer()

        if instance.public:
            async_to_sync(channel_layer.group_send)(common_channel, event)

        elif instance.recipient_id:
            user_channel = f"user_{instance.recipient_id}"
            async_to_sync(channel_layer.group_send)(user_channel, event)


def notify_instance_to_data(instance):
    return {
        'title': instance.verb,
        'description': instance.description,
        'timesince': timesince(instance.timestamp),
        'slug': instance.slug,
        'unread': instance.unread,
        'public': instance.public
    }

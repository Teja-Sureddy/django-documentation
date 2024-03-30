from notifications.utils import slug2id
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from django.http import JsonResponse


def notification_read_view(request, slug=None):
    if request.method == 'POST':
        notification_id = slug2id(slug)
        notification = get_object_or_404(Notification, recipient=request.user, id=notification_id)
        notification.mark_as_read()
        return JsonResponse({'success': True}, status=200)

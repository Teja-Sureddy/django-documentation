from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_apps.notification'

    def ready(self):
        import my_apps.notification.signals

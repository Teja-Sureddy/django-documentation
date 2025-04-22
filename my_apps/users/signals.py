"""
Signals let you run specific code automatically when certain actions or events (before or after) happen in your app.
You need to ready the signals from apps.py.

Signals:

django.contrib.auth.signals
django.db.models.signals
django.db.backends.signals
django.core.signals

allauth.account.signals
allauth.mfa.signals
allauth.socialaccount.signals
channels.signals
more...
"""

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.db.models.signals import post_save
from my_apps.users.models.user import User


@receiver(user_logged_in)
def post_logged_in(sender, user, request, **kwargs):
    print(f"User {user.email} has logged in.")


@receiver(user_logged_out)
def post_logged_out(sender, user, request, **kwargs):
    print(f"User {user.email} has logged out.")


@receiver(post_save, sender=User)
def notify_user_created(sender, instance, created, **kwargs):
    if created:
        print(f"User {instance.email} has been created.")

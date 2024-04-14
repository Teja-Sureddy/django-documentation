"""
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


@receiver(user_logged_in)
def post_logged_in(sender, user, request, **kwargs):
    print(f"User {user.email} has logged in.")


@receiver(user_logged_out)
def post_logged_out(sender, user, request, **kwargs):
    print(f"User {user.email} has logged out.")

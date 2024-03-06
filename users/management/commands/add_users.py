from django.core.management.base import BaseCommand
from users.models import User
import random
import string


class Command(BaseCommand):
    help = 'Inserts dummy Users'

    def handle(self, *args, **options):
        admin = {'name': 'admin', 'password': 'admin', 'email': 'admin@gmail.com', 'phone': '8888888888'}
        try:
            User.objects.create_superuser(**admin)
            print('admin Done.')
        except:
            pass

        user = {'name': 'test', 'password': 'test', 'email': 'test@gmail.com', 'phone': '9999999999'}
        try:
            User.objects.create_user(**user)
            print('test Done.')
        except:
            pass

from django.core.management.base import BaseCommand
from users.models import User
import random
import string


class Command(BaseCommand):
    help = 'Inserts dummy Users'

    def handle(self, *args, **options):
        admin = {'name': 'admin', 'password': 'admin', 'email': 'admin@gmail.com', 'phone': '9876543210'}
        try:
            User.objects.create_superuser(**admin)
            print('admin Done.')
        except:
            pass

        user = {'name': 'user', 'password': 'useruser', 'email': 'user@gmail.com', 'phone': '9999999999'}
        try:
            User.objects.create_user(**user)
            print('user Done.')
        except:
            pass

        for i in range(1, 10):
            phone = random.randint(1000000000, 9999999999)
            password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

            data = {'name': f'user_{i}', 'password': password, 'email': f'user-{i}@gmail.com', 'phone': str(phone)}
            try:
                User.objects.create_user(**data)
            except:
                pass
        print('all Done.')

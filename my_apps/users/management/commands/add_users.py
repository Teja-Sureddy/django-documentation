from django.core.management.base import BaseCommand
from my_apps.users.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    help = 'Inserts dummy Users'

    def handle(self, *args, **options):
        admin_data = {'name': 'admin', 'password': 'admin', 'email': 'admin@gmail.com', 'phone': '8888888888'}
        try:
            User.objects.create_superuser(**admin_data)
            print('admin user created.')
        except:
            pass

        user_data = {'name': 'test', 'password': 'test', 'email': 'test@gmail.com', 'phone': '9999999999'}
        user, created = User.objects.get_or_create(email=user_data['email'], defaults=user_data)
        if created:
            EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
            print('test user created.')

        content_type = ContentType.objects.get(app_label='auth', model='permission')

        permission_codenames = ['post_data', 'delete_data']
        permissions = []
        for codename in permission_codenames:
            permission, created = Permission.objects.get_or_create(
                codename=codename, content_type=content_type, defaults={'name': f'Can {codename.replace("_", " ")}'}
            )
            permissions.append(permission)
            if created:
                print('permissions created')

        for permission in permissions:
            user.user_permissions.add(permission)
        print('permissions added')

        self.stdout.write(self.style.SUCCESS('Successfully inserted user data.'))

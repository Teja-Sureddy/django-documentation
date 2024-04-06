from django.core.management.base import BaseCommand
from notifications.models import Notification
from my_apps.users.models import User
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Inserts dummy Notifications'

    def handle(self, *args, **options):
        user = User.objects.get(pk=2)
        content_type = ContentType.objects.get(app_label='notifications', model='notification')

        notification_data = [
            Notification(recipient=user, actor_content_type=content_type, public=False, verb='What is Lorem Ipsum?',
                         description='''Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
                         Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown 
                         printer took a galley of type and scrambled it to make a type specimen book. It has survived 
                         not only five centuries, but also the leap into electronic typesetting, remaining essentially 
                         unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem 
                         Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker 
                         including versions of Lorem Ipsum.'''),
            Notification(recipient=user, actor_content_type=content_type, verb='Small notification',
                         description='Hello There!'),
            Notification(recipient=user, actor_content_type=content_type,
                         verb='Section 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC',
                         description='''Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium 
                         doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi 
                         architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit 
                         aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem 
                         sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, 
                         adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam 
                         aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam 
                         corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum 
                         iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum 
                         qui dolorem eum fugiat quo voluptas nulla pariatur?'''),
            Notification(recipient=user, actor_content_type=content_type, public=False, verb='Section',
                         description='1.10.32'),
            Notification(recipient=user, actor_content_type=content_type, public=False, verb='Why do we use it?',
                         description='''It is a long established fact that a reader will be distracted by the readable 
                         content of a page when looking at its layout.'''),
        ]

        for notification in notification_data:
            notification.save()

        self.stdout.write(self.style.SUCCESS('Successfully inserted notification data.'))

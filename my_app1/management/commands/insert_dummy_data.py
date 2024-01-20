import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from my_app1.models import MyModel1, MyModel2, MyModel3, MyModel4
import string
import ipaddress
from datetime import timedelta


def generate_random_ip():
    ip = ipaddress.ip_address('.'.join(str(random.randint(1, 255)) for _ in range(4)))
    return str(ip)


def generate_random_website():
    domain_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 10)))
    tld = random.choice(['com', 'org', 'net', 'edu', 'gov'])
    return f"http://{domain_name}.{tld}"


def generate_random_duration():
    days = random.randint(0, 365)
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    seconds = random.randint(0, 59)

    duration = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return duration


class Command(BaseCommand):
    help = 'Inserts dummy data into MyModel1, MyModel2, MyModel3, and MyModel4'

    def handle(self, *args, **options):
        # Insert dummy data into MyModel1
        for _ in range(10):
            rand = random.randint(1, 100)
            existing_instance = MyModel1.objects.filter(email=f'person_{rand}@example.com').first()

            if existing_instance is None:
                MyModel1.objects.create(
                    name=f'Person {rand}',
                    email=f'person_{rand}@example.com',
                    age=random.randint(18, 50),
                    dob=timezone.now().date(),
                    tob=timezone.now().time(),
                    gender=random.choice(['M', 'F']),
                    ip_address=generate_random_ip(),
                    website=generate_random_website()
                )
        print('MyModel1 Done.')

        # Insert dummy data into MyModel2
        favorite_colors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple']
        for _ in range(5):
            favorite_color = random.choice(favorite_colors)
            MyModel2.objects.create(favorite_color=favorite_color)
        print('MyModel2 Done.')

        # Insert dummy data into MyModel3
        for _ in range(7):
            MyModel3.objects.create(
                is_hair_styled=random.choice([True, False]),
                hair_length_cm=random.randint(20, 50),
                hair_color_intensity=random.uniform(0.1, 3.0),
                hair_shine_factor=random.uniform(0.1, 1.0),
                hair_description=f'Dummy description {_}'
            )
        print('MyModel3 Done.')

        # Insert dummy data into MyModel4
        my_model1_instances = MyModel1.objects.all()
        my_model2_instances = MyModel2.objects.all()
        my_model3_instances = MyModel3.objects.all()

        for _ in range(10):
            my_model1_instance = random.choice(my_model1_instances)
            existing_instance = MyModel4.objects.filter(my_model1=my_model1_instance).first()
            data = {
                "name": ''.join(random.choice(string.ascii_letters) for _ in range(10)),
                "age": random.randint(18, 60),
                "is_student": random.choice([True, False]),
                "grades": [random.randint(60, 100) for _ in range(5)]
            }

            if existing_instance is None:
                MyModel4.objects.create(
                    hair_color=random.choice(['BL', 'BR', 'BK', 'RD', 'OT']),
                    duration=str(generate_random_duration()),
                    json_data=data,
                    my_model1=my_model1_instance,
                    my_model3=random.choice(my_model3_instances)
                ).my_model2.set(random.sample(list(my_model2_instances), random.randint(1, 3)))
        print('MyModel4 Done.')

        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy data.'))

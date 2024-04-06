import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from my_apps.dashboard.models import Data, Color, Hair, FullData
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
    help = 'Inserts dummy data into Data, Color, Hair, and FullData'

    def handle(self, *args, **options):
        # Insert dummy data into Data
        for _ in range(1000):
            rand = random.randint(1000, 9999)
            existing_instance = Data.objects.filter(email=f'person_{rand}@example.com').first()

            if existing_instance is None:
                Data.objects.create(
                    name=f'Person {rand}',
                    email=f'person_{rand}@example.com',
                    age=random.randint(10, 60),
                    dob=timezone.now().date(),
                    tob=timezone.now().time(),
                    gender=random.choice(['M', 'F']),
                    ip_address=generate_random_ip(),
                    website=generate_random_website()
                )
        print('Data Done.')

        # Insert dummy data into Color
        favorite_colors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple']
        for _ in range(20):
            favorite_color = random.choice(favorite_colors)
            Color.objects.create(favorite_color=favorite_color)
        print('Color Done.')

        # Insert dummy data into Hair
        for _ in range(200):
            Hair.objects.create(
                is_hair_styled=random.choice([True, False]),
                hair_length_cm=random.randint(20, 50),
                hair_color_intensity=random.uniform(0.1, 3.0),
                hair_shine_factor=random.uniform(0.1, 1.0),
                hair_description=f'Dummy description {_}'
            )
        print('Hair Done.')

        # Insert dummy data into FullData
        data_instances = Data.objects.all()
        color_instances = Color.objects.all()
        hair_instances = Hair.objects.all()

        for _ in range(1000):
            data_instance = random.choice(data_instances)
            existing_instance = FullData.objects.filter(data=data_instance).first()
            data = {
                "name": ''.join(random.choice(string.ascii_letters) for _ in range(10)),
                "age": random.randint(18, 60),
                "is_student": random.choice([True, False]),
                "grades": [random.randint(60, 100) for _ in range(5)]
            }

            if existing_instance is None:
                FullData.objects.create(
                    hair_color=random.choice(['BL', 'BR', 'BK', 'RD', 'OT']),
                    duration=str(generate_random_duration()),
                    json_data=data,
                    data=data_instance,
                    hair=random.choice(hair_instances)
                ).color.set(random.sample(list(color_instances), random.randint(1, 3)))
        print('FullData Done.')

        self.stdout.write(self.style.SUCCESS('Successfully inserted dummy data.'))

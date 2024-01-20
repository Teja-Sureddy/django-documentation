from django.db import models
from django.utils import timezone
import uuid
from django.utils.text import slugify


# Create your models here.
class MyModel1(models.Model):
    GENDERS = [("M", "Male"), ("F", "Female")]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    dob = models.DateField()
    tob = models.TimeField()
    gender = models.CharField(max_length=1, choices=GENDERS)
    ip_address = models.GenericIPAddressField()
    slug = models.SlugField()
    website = models.URLField()
    identity = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.slug:
            # It replaces spaces with hyphens, removes special characters, and converts the string to lowercase
            self.slug = slugify(self.email)
        super().save(*args, **kwargs)


class MyModel2(models.Model):
    favorite_color = models.CharField(max_length=50, default='Blue')

    def __str__(self):
        return self.favorite_color


class MyModel3(models.Model):
    is_hair_styled = models.BooleanField(default=False)
    hair_length_cm = models.IntegerField(default=0)
    hair_color_intensity = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    hair_shine_factor = models.FloatField(default=0.0)
    hair_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.is_hair_styled}, Length: {self.hair_length_cm}cm, Intensity: {self.hair_color_intensity}, " \
               f"Shine: {self.hair_shine_factor}, Description: {self.hair_description}"


class MyModel4(models.Model):
    class HairColor(models.TextChoices):
        BLONDE = 'BL', 'Blonde'
        BROWN = 'BR', 'Brown'
        BLACK = 'BK', 'Black'
        RED = 'RD', 'Red'
        OTHER = 'OT', 'Other'

    hair_color = models.CharField(blank=True, choices=HairColor.choices, max_length=2)
    duration = models.DurationField()
    json_data = models.JSONField(blank=True, null=True)
    my_model1 = models.OneToOneField(MyModel1, on_delete=models.CASCADE)
    my_model2 = models.ManyToManyField(MyModel2)
    my_model3 = models.ForeignKey(MyModel3, on_delete=models.CASCADE)  # It is many-to-one

    def __str__(self):
        return f"{self.my_model1.name}'s hair color: {self.hair_color}"


class UploadModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    file_field = models.FileField(upload_to='files/')
    image_field = models.ImageField(upload_to='images/')
    # contains all params
    description = models.TextField(
        blank=False,
        null=False,
        default='',
        validators=[],
        help_text='Enter a description.',
        verbose_name='File Description',
        unique=False,
        error_messages={'invalid': 'Invalid description. Please provide valid text.'}
    )

    def __str__(self):
        return self.name

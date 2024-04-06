from django.db import models
from django.utils import timezone
import uuid
from django.utils.text import slugify


class Data(models.Model):
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

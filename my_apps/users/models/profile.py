from django.db import models
from my_apps.users.models import User


def get_proof_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % ('proof', ext)
    return f'proofs/{instance.user.id}/{new_filename}'


def get_profile_pic_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % ('profile_pic', ext)
    return f'profile_pics/{instance.user.id}/{new_filename}'


def get_profile_thumb_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s.%s" % ('profile_thumb', ext)
    return f'profile_thumbs/{instance.user.id}/{new_filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    proof = models.FileField(upload_to=get_proof_path, null=True)
    profile_pic = models.ImageField(upload_to=get_profile_pic_path, null=True)
    profile_thumb = models.ImageField(upload_to=get_profile_thumb_path, null=True)
    # description contains all params
    description = models.TextField(
        blank=False,
        null=True,
        default='',
        validators=[],
        help_text='Enter a description.',
        verbose_name='File Description',
        unique=False,
        error_messages={'invalid': 'Invalid description. Please provide valid text.'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

from django.db import models
from dashboard.models import DataModel


class UploadDocumentsModel(models.Model):
    data = models.OneToOneField(DataModel, on_delete=models.CASCADE, unique=True)
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
        return self.data.name

from django.db import models
from my_apps.dashboard.models import DataModel, ColorModel, HairModel


class FullDataModel(models.Model):
    class HairColor(models.TextChoices):
        BLONDE = 'BL', 'Blonde'
        BROWN = 'BR', 'Brown'
        BLACK = 'BK', 'Black'
        RED = 'RD', 'Red'
        OTHER = 'OT', 'Other'

    hair_color = models.CharField(blank=True, choices=HairColor.choices, max_length=2)
    duration = models.DurationField()
    json_data = models.JSONField(blank=True, null=True)
    data = models.OneToOneField(DataModel, on_delete=models.CASCADE)
    color = models.ManyToManyField(ColorModel)
    hair = models.ForeignKey(HairModel, on_delete=models.CASCADE)  # It is many-to-one

    def __str__(self):
        return f"{self.data.name}'s hair color: {self.hair_color}"

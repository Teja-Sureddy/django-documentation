from django.db import models


class Hair(models.Model):
    is_hair_styled = models.BooleanField(default=False)
    hair_length_cm = models.IntegerField(default=0)
    hair_color_intensity = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    hair_shine_factor = models.FloatField(default=0.0)
    hair_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.is_hair_styled}, Length: {self.hair_length_cm}cm, Intensity: {self.hair_color_intensity}, " \
               f"Shine: {self.hair_shine_factor}, Description: {self.hair_description}"

from django.db import models


class Color(models.Model):
    favorite_color = models.CharField(max_length=50, default='Blue')

    def __str__(self):
        return self.favorite_color

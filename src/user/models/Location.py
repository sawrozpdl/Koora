from django.db import models
from django.conf import settings

class Location(models.Model):

    country = models.CharField(max_length=2, choices=settings.COUNTRIES, default='NP', blank=True)
    address = models.CharField(max_length=250,  default="")
    city = models.CharField(max_length=250,  default="")
    province = models.CharField(max_length=250,  default="")
    zip_code = models.CharField(max_length=250,  default="")

    def __str__(self):
        return str(self.city)

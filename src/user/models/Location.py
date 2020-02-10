from django.db import models


class Location(models.Model):

    country = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=250, null=True)
    province = models.CharField(max_length=250, null=True)
    zip_code = models.CharField(max_length=250, null=True)

    def __str__(self):
        return str(self.city)

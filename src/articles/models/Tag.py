from django.db import models

class Tag(models.Model):

    name = models.CharField(max_length=60)
    description = models.CharField(max_length=320)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True)

    def __unicode__():
        return self.name

    def __str__(self):
        return self.name
    
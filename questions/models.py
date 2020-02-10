from django.db import models
from articles.models import Koora
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


class Questions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    Create_Question = models.TextField(max_length=500)
    Elaborate_Question=models.TextField(max_length=500)
    published_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    avatar_url = models.URLField(blank=True, null=True, max_length=300)


class Profile(models.model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250)
    birth_date = models.DateField(null=True, blank=True)
    

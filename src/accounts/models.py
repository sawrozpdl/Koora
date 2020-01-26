from django.db import models
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
#     avatar_url = models.URLField(blank=True, null=True, max_length=300)

#     class Meta:
#         abstract = True


# class Profile(models.model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.CharField(max_length=250)
#     intrests = models.CharField(max_length=250)
#     location = models.CharField(max_length=50)

#     class Meta:
#         abstract = True
    

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     # User = models.OneToOneField(Profile, on_delete=models.CASCADE)
#     avatar_url = models.URLField(blank=True, null=True, max_length=300)

class Profile(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    bio = models.CharField(max_length=250)
    intrests = models.CharField(max_length=250)
    location = models.CharField(max_length=50)
    

    def __str__(self):
        return self.user.username





    

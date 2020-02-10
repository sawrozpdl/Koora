from django.db import models
from articles.models import Tag
from .Card import *
from .Location import *
from .Social import *
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class ProfileManager(models.Manager):

  pass




class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    avatar_url = models.URLField(blank=True, null=True)
    is_private = models.BooleanField(default=True)
    birth_date = models.DateTimeField(blank=True, null=True)

    intro = models.CharField(max_length=250, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)

    interests = models.ManyToManyField(Tag)
    
    location = models.OneToOneField(Location, on_delete=models.CASCADE)

    social = models.OneToOneField(Social, on_delete=models.CASCADE)

    card = models.OneToOneField(Card, on_delete=models.CASCADE, blank=True, null=True)


    objects = ProfileManager()

    

    def __str__(self):
      return self.user.username


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
      if created:
        Profile.objects.create(
          user=instance,
          location=Location.objects.create(),
          social=Social.objects.create()
        )

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
      if hasattr(instance, 'profile'):
        instance.profile.save()

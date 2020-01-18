from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class VoteManager(models.Manager):

    def of_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return super(VoteManager, self).filter(content_type=content_type, object_id= object_id)


class Vote(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_upvote = models.BooleanField(default=True)
    voted_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = VoteManager()
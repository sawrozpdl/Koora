from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class VoteManager(models.Manager):

    def of_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return super(VoteManager, self).filter(content_type=content_type, object_id=object_id)



class Vote(models.Model):
    object_id = models.PositiveIntegerField()
    is_upvote = models.BooleanField(default=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    voted_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = VoteManager()

    def vote_type_for(self, user):
        return self.is_upvote if self.user == user else -1

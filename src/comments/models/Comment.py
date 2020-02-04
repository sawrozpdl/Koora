from articles.models import Koora, KooraManager
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from articles.models import Vote


class CommentManager(KooraManager):

    def parents(self):
        return super(CommentManager, self).filter(parent=None)

    def all_of_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return super(CommentManager, self).filter(content_type=content_type, object_id= object_id)

    def of_instance(self, instance):
        return self.all_of_instance(instance).filter(parent=None)


class Comment(Koora):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    objects = CommentManager()

    def __str__(self):
        return str(self.user.username)

    @property
    def delete_url(self):
        return reverse("comments:delete", kwargs={"slug": self.slug})

    @property  
    def children(self): 
        return Comment.objects.filter(parent=self)
    
    @property
    def voters(self, is_upvote):
        return Vote.objects.of_instance(self).filter(is_upvote=is_upvote)

    @property
    def is_parent(self):
        return self.parent is None
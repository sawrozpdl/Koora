from django.db import models
from django.urls import reverse
from django.conf import settings

from django.forms.models import model_to_dict
from articles.models import Koora, KooraManager
from articles.models.Vote import Vote
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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

    class Meta:
        ordering = ['published_at']

    def __str__(self):
        return str(self.user.username)

    @property  
    def children(self): 
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        return self.parent is None

    @property
    def c_type(self):
        return ContentType.objects.get_for_model(self.__class__)

    @property
    def parent_content_type(self):
        return ContentType.objects.get_for_model(self.content_object.__class__)

    # @property
    # def parent_content_slug(self):
    #     return self.content_object.slug


    @property
    def all_votes(self):
        return Vote.objects.of_instance(self)

    @property
    def up_votes(self):
        return Vote.objects.of_instance(self).filter(is_upvote=True)
    
    @property
    def down_votes(self):
        return Vote.objects.of_instance(self).filter(is_upvote=False)


    def get_user_vote(self, user):
        votes = Vote.objects.of_instance(self)
        for vote in votes:
            vote_type = vote.vote_type_for(user)
            if vote_type != -1:
                return vote_type
        return None


    @property
    def vote_count(self):
        return self.up_votes.count() - self.down_votes.count()
        

    def to_dict(self):
        ignore_fields = ['objects', 'up_votes', 'down_votes', 'content_object', 'parent']
        db_dict = model_to_dict(self)
        for attr in dir(self):
             if not attr.startswith('_') and not attr in ignore_fields and not callable(getattr(self, attr)) and not attr in dir(db_dict):
                db_dict[attr] = getattr(self, attr)
        return db_dict
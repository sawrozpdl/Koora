from . import Koora
from .Vote import *
from . import KooraManager
from django.db import models
from django.urls import reverse
from django.conf import settings
from comments.models.Comment import *
from django.forms.models import model_to_dict
from django.contrib.contenttypes.models import ContentType

class ArticleManager(KooraManager):

    def of_category(self, category_key, *args, **kwargs):
        return super(ArticleManager, self).filter(category=category_key)


class Article(Koora):

    category = models.CharField(max_length=2, choices=settings.KOORA_CATEGORIES, default='RN', blank=True)

    objects = ArticleManager()

    @property
    def absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})

    @property
    def update_url(self):
        return reverse("articles:update", kwargs={"slug": self.slug})


    @property
    def comments(self):
        return Comment.objects.of_instance(self)

    @property
    def all_comments(self):
        return Comment.objects.all_of_instance(self).count()

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

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.__class__)

    @property
    def c_type(self):
        return ContentType.objects.get_for_model(self.__class__)
        

    #   marking the markdown safe prevents django from messing with it for protection

    def contains_tag(self, tag):
        return (tag.lower() in self.title.lower()) | (tag.lower() in self.content.lower())

    def has_tag(self, tag_name):
        for local_tag in self.tags.all():
            if local_tag.name == tag_name:
                return True
        return False

    @property
    def tag_string(self):
        req = ''
        for tag in self.tags.all():
            req += tag.name + ','
        return req

    def remove_tags(self):
        for tag in self.tags.all():
            self.tags.remove(tag)


    def to_dict(self):
        ignore_fields = ['objects', 'up_votes', 'down_votes']
        db_dict = model_to_dict(self)
        for attr in dir(self):
             if not attr.startswith('_') and not attr in ignore_fields and not callable(getattr(self, attr)) and not attr in dir(db_dict):
                db_dict[attr] = getattr(self, attr)
        return db_dict
        


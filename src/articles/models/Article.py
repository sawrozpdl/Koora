from . import Koora
from . import KooraManager
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from django.urls import reverse
from comments.models.Comment import *
from .Vote import *

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
    def voters(self, is_upvote):
        return Vote.objects.of_instance(self).filter(is_upvote=is_upvote)


    #   marking the markdown safe prevents django from messing with it for protection

    @property
    def get_markdown(self):
        return mark_safe(markdown(self.content))

    def contains_tag(self, tag):
        return (tag.lower() in self.title.lower()) | (tag.lower() in self.content.lower())

    def get_tag_string(self):
        req = ''
        for tag in self.tags.all():
            req += tag.name + ', '
        return req[:(len(req) - 2)]

    def remove_tags(self):
        for tag in self.tags.all():
            self.tags.remove(tag)
        
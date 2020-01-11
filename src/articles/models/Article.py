from . import Koora
from . import KooraManager
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from django.urls import reverse

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


    #   marking the markdown safe prevents django from messing with it for protection

    @property
    def get_markdown(self):
        return mark_safe(markdown(self.content))
        
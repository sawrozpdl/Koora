from django.conf import settings
from django.utils.text import slugify
from django.db import models
from django.contrib.contenttypes.models import ContentType
from .Tag import *

class KooraManager(models.Manager):

    def private(self, user = None):
        to_return = super(KooraManager, self).filter(is_private=True)
        return to_return.filter(user=user) if user else to_return

    def public(self, user = None):
        to_return = super(KooraManager, self).filter(is_private=False, is_drafted=False)
        return to_return.filter(user=user) if user else to_return
    
    def drafted(self, user = None):
        to_return = super(KooraManager, self).filter(is_drafted=True)
        return to_return.filter(user=user) if user else to_return

    def active(self, user=None):
        to_return = super(KooraManager, self).filter(is_drafted=False)
        return to_return.filter(user=user) if user else to_return


class Koora(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    image_url = models.URLField(blank=True, null=True, max_length=300)
    content = models.TextField()
    is_drafted = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    published_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = KooraManager()

    class Meta:
        abstract = True
        ordering = ['-updated_at']

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_unique_slug(self, text, custom_slug=None):
        slug = slugify(text)
        if custom_slug is not None:
            slug = custom_slug
        repetition = self.__class__.objects.filter(slug=slug).order_by("-id")
        if repetition.exists():
            custom_slug = "%s-%s" % (slug, repetition.first().id)
            return self.get_unique_slug(text, custom_slug=custom_slug)
        return slug


    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.__class__)

    @property
    def user_avatar_url(self):
        return self.user.profile.avatar_url if hasattr(self.user, 'profile') else None

    def save(self, **kwargs):
        if not self.slug:
            payload = self.title if self.title else self.content
            self.slug = self.get_unique_slug(payload)
        super(Koora, self).save(**kwargs)
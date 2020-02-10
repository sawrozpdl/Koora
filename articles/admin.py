from django.contrib import admin

# Register your models here.

from .models import Article
from .models import Tag
from .models import Vote

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Vote)
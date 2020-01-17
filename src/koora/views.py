from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from articles.models import Tag

def index(request):
    popular_tags = Tag.objects.all()
    return HttpResponse(loader.get_template('base.html').render({
            "page_name" :  'home',
            "popular_tags" : popular_tags,
            "categories" : settings.KOORA_CATEGORIES
        }, request))
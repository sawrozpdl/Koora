from django.http import HttpResponse
from django.template import loader
from django.conf import settings

def index(request):
    return HttpResponse(loader.get_template('base.html').render({
            "categories" : settings.KOORA_CATEGORIES
        }, request))
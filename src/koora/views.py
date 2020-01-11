from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import os

def index(request):
    return HttpResponse(loader.get_template('base.html').render({
            "categories" : settings.KOORA_CATEGORIES
        }, request))

def read_file(request,filename):
   f = open(filename,'r')
   file_content = f.read()
   f.close()
   return HttpResponse(file_content, content_type="text/plain")

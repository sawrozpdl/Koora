from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse(loader.get_template('base.html').render({
            "page_name" :  'home'
    }, request))


def csrf_fail(request, reason):
    return HttpResponse(loader.get_template('403.html').render({
            "page_name" :  '403',
            "reason" : reason
    }, request))
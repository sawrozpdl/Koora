from django.views import View 
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError

class CreateView(View):

    def get(self, request):
        return HttpResponse(loader.get_template('questions/create_question.html').render({
            "page_name" : "ask_question",
            "messages" : [
                {
                    "type" : "warning",
                    "content" : "Fill up the ask question field"
                }
            ],
            "categories" : settings.KOORA_CATEGORIES
        }, request))
from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from django.conf import settings
from ..models import Questions
from utils.pages import Paginator


class ListView(View):

    def get(self, request):
        
        required_questions = Questions.objects.all()

        template = loader.get_template("questions/questions.html")

        try:    
            page = int(request.GET.get("page", 1))
        except:
            page = 1
        try:
            size = int(request.GET.get("size", 3))
        except:
            size = 3
        paginator = Paginator(required_questions, size)
        content = {
            "page_name": "questions",
            "title" : "Questions:",
            "page" : paginator.page(page) if required_questions else None,
            "page_range" : paginator.page_range() if required_questions else None,
            "hasResults" : True if (len(required_questions) > 0) else False
        }
        return HttpResponse(template.render(content, request))

    def post(self, request):
        pass


#TODO SEPERATE THIS FROM HERE

def getValueFor(reqKey, choices=settings.KOORA_CATEGORIES):
    values = {key : value for key, value in choices}
    return values[reqKey]
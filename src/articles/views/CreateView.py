from django.views import View
from django.template import loader
from django.http import HttpResponse

class CreateView(View):

    def get(self, request):
        return HttpResponse(loader.get_template('articles/create_article.html').render({
            "guide" : "Create your article"
        }, request))

    def post(self, request):
        return HttpResponse(loader.get_template("articles/create_article.html").render({
            "success" : "Article creation successful!"
        }, request))
from django.views import View
from django.template import loader
from django.http import HttpResponse
from articles.models import Article

class DetailView(View):

    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        template = loader.get_template("articles/article.html")
        content = {
            "article": article
        }
        return HttpResponse(template.render(content, request))

    def post(self, request, slug):
        article = Article.objects.get(slug=slug)
        article.delete()
        articles = Article.objects.all()
        template = loader.get_template("articles/articles.html")
        content = {
            "title" : "Articles by Users:",
            "articles" : articles,
            "success" : "Article deletion successfull!"
        }
        return HttpResponse(template.render(content, request))
        

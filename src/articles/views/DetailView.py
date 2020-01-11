from django.views import View
from django.template import loader
from django.http import HttpResponse


dummy = {
            "article_id" : 2,
            "dateCreated" : 2012,
            "dateUpdated" : 2018,
            "title" : "title lol",
            "content" : "this is contetn"
        }

class DetailView(View):

    def get(self, request, article_id):
        article = dummy
        template = loader.get_template("articles/article.html")
        content = {
            "article": article
        }
        return HttpResponse(template.render(content, request))

    def post(self, request, article_id):
        articles = [dummy, dummy, dummy, dummy, dummy, dummy, dummy]
        template = loader.get_template("articles/articles.html")
        content = {
            "title" : "Articles by Users:",
            "articles" : articles,
            "success" : "todo deletion successfull!"
        }
        return HttpResponse(template.render(content, request))
        

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

class ListView(View):

    def get(self, request):
        searchQuery = request.POST.get("searchQuery", False)  # False is default when there"s no search
        articles = [dummy, dummy, dummy, dummy, dummy, dummy, dummy]
        template = loader.get_template("articles/articles.html")
        content = {
            "title" : "articles by Users:",
            "articles" : articles,
            "searchQuery" : request.POST.get("searchQuery", False),
            "hasResults" : True if (len(articles) > 0) else False
        }
        return HttpResponse(template.render(content, request))

    def post(self, request):
        pass
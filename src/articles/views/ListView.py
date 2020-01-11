from django.views import View
from django.template import loader
from django.http import HttpResponse
from ..models import Article


class ListView(View):

    def get(self, request):
        searchQuery = request.POST.get("searchQuery", False)  # False is default when there"s no search
        articles = list(Article.objects.all())
        template = loader.get_template("articles/articles.html")
        content = {
            "title" : "Articles by Users on Koora:",
            "articles" : articles,
            "searchQuery" : request.POST.get("searchQuery", False),
            "hasResults" : True if (len(articles) > 0) else False
        }
        return HttpResponse(template.render(content, request))

    def post(self, request):
        pass
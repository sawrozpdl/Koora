from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from django.conf import settings
from ..models import Article
from ..models import Tag

class ListView(View):

    def get(self, request):
        try:
            searchQuery = request.GET.get("searchQuery", False)  # False is default when there"s no search
            tag = request.GET.get("tag", False)  
            category = request.GET.get("category", False)  # False is default when there"s no search
            articles = Article.objects.all()
            required_articles = articles
            query = {}
            if searchQuery:
                required_articles = list(filter(lambda article : article.contains_tag(searchQuery), Article.objects.all()))
                query = {
                    "searchQuery" : searchQuery
                }
            elif category:
                required_articles = list(Article.objects.filter(category=category))
                query = {
                    "category" : getValueFor(category)
                }
            elif tag:
                required_articles = list(Tag.objects.get(name=tag).article_set.all())
                query = {
                    "tag" : tag
                }
            template = loader.get_template("articles/articles.html")
            content = {
                "page_name": "articles",
                "title" : "Articles from Koora Users:",
                "articles" : required_articles,
                "query" : query.items(),
                "hasResults" : True if (len(required_articles) > 0) else False
            }
            return HttpResponse(template.render(content, request))
        except:
            return HttpResponseServerError()

    def post(self, request):
        pass


#TODO SEPERATE THIS FROM HERE

def getValueFor(reqKey, choices=settings.KOORA_CATEGORIES):
    values = {key : value for key, value in choices}
    return values[reqKey]
from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from django.conf import settings
from ..models import Article
from ..models import Tag
from utils.pages import Paginator
from utils.decorators import fail_safe

class ListView(View):

    @fail_safe(for_model=Article)
    def get(self, request):
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

        try:
            page = int(request.GET.get("page", 1))
        except:
            page = 1
        try:
            size = int(request.GET.get("size", 3))
        except:
            size = 3
        paginator = Paginator(required_articles, size)
        content = {
            "page_name": "articles",
            "title" : "Articles from Koora Users:",
            "page" : paginator.page(page) if required_articles else None,
            "page_range" : paginator.page_range() if required_articles else None,
            "query" : query.items(),
            "hasResults" : True if (len(required_articles) > 0) else False
        }
        return HttpResponse(template.render(content, request))

    def post(self, request):
        pass


#TODO SEPERATE THIS FROM HERE

def getValueFor(reqKey, choices=settings.KOORA_CATEGORIES):
    values = {key : value for key, value in choices}
    return values[reqKey]
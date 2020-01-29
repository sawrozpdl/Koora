from django.views import View
from django.template import loader
from django.http import HttpResponse
from ..models import Article
from ..models import Tag
from utils.pages import Paginator
from utils.koora import getValueFor, get_message_or_default
from utils.decorators import fail_safe

class ListView(View):

    #@fail_safe(for_model=Article)
    def get(self, request):

        searchQuery = request.GET.get("searchQuery", False)
        tag = request.GET.get("tag", False)  
        category = request.GET.get("category", False)

        message = get_message_or_default(request, {})

        articles = Article.objects.public()
        required_articles = articles


        query = {}
        if searchQuery:
            required_articles = list(filter(lambda article : article.contains_tag(searchQuery), required_articles))
            query = {
                "searchQuery" : searchQuery
            }
        if category:
            required_articles = list(filter(lambda article : article.category == category, required_articles))
            query = {
                "category" : getValueFor(category)
            }
        if tag:
            required_articles = list(filter(lambda article : article.has_tag(tag), required_articles))
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
            "message" : message,
            "page" : paginator.page(page) if required_articles else None,
            "page_range" : paginator.page_range() if required_articles else None,
            "query" : query.items(),
            "hasResults" : True if (len(required_articles) > 0) else False
        }

        return HttpResponse(template.render(content, request))

    def post(self, request):
        pass
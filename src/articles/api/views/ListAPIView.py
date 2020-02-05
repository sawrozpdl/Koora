from django.views import View
from articles.models import Tag
from utils.pages import Paginator
from django.template import loader
from articles.models import Article
from django.http import JsonResponse
from utils.decorators import fail_safe_api
from utils.request import parse_body, set_user
from utils.models import nested_model_to_dict
from utils.koora import getValueFor, get_message_or_default, setTagsFor

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class ListAPIView(View):


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            set_user(request)
        except Exception:
            return JsonResponse({
                'status' : 403
            })
        parse_body(request, for_method=request.method)
        return super(ListAPIView, self).dispatch(request, *args, **kwargs)



    #@fail_safe_api(for_model=Article)
    def get(self, request):

        searchQuery = request.GET.get("searchQuery", False)
        tag = request.GET.get("tag", False)  
        category = request.GET.get("category", False)

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

        articles_count = len(required_articles)

        required_page = paginator.page(page)

        content = {
            "status" : 200,
            "page" : nested_model_to_dict(required_page),
            "page_range" : list(paginator.page_range()) if required_articles else None,
            "query" : query,
            "hasResults" : (articles_count > 0),
            "meta" : {
                "count" : articles_count
            }
        }

        return JsonResponse(content)


    #@fail_safe_api(for_model=Article)
    #@protected_view_api(allow='logged_users')
    def post(self, request):
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        image = request.FILES.get('article_image', False)

        post_type=request.POST.get('post_type', 'public')
        post_mode=request.POST.get('post_mode', 'publish')

        is_private = post_type == 'private'
        is_drafted = post_mode == 'draft'

        article = Article.objects.create(user=request.user, title=title, content=content, category=category, is_drafted = is_drafted, is_private=is_private)

        # if (image):
        #     uploadImageFor(article, image, request.user.username)
            
        tags = request.POST.get('tags', '').strip().split(",")
        
        setTagsFor(article, tags)
            
        article.save()

        content = {
            "status": 200,
            "message" : "article {}".format('drafted' if is_drafted else 'created'),
            "data": {
                "article": nested_model_to_dict(article)
            },
            "meta": {
                "count": 1,
            }
        }

        return JsonResponse(content)

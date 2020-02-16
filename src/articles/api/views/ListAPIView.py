from django.contrib.auth.models import User
from django.views import View
from articles.models import Tag
from utils.pages import Paginator
from django.template import loader
from articles.models import Article
from django.http import JsonResponse
from utils.decorators import fail_safe_api
from utils.models import nested_model_to_dict
from utils.request import parse_body, set_user
from utils.koora import getValueFor, setTagsFor, uploadImageFor


class ListAPIView(View):


    def dispatch(self, request, *args, **kwargs):
        set_user(request)
        if request.user.is_authenticated:
            parse_body(request, for_method=request.method)
        return super(ListAPIView, self).dispatch(request, *args, **kwargs)



    @fail_safe_api(for_model=Article)
    def get(self, request):

        searchQuery = request.GET.get("searchQuery", False)
        tag = request.GET.get("tag", False)
        category = request.GET.get("category", False)

        user=request.user

        visitee=None

        uid = request.GET.get("uid", False)

        if uid:
            visitee = User.objects.get(id=uid)

        is_viewing_self = (user.username == visitee.username) if visitee else True

        atype = request.GET.get('atype', False) if is_viewing_self else 'public'

        to_show = visitee if uid else user

        required_articles = getattr(Article.objects, atype or 'public')(user=to_show if atype else None)

        query = {}

        if searchQuery:
            required_articles = list(filter(lambda article : article.contains_tag(searchQuery), required_articles))
            query['searchQuery'] = searchQuery

        if category:
            required_articles = list(filter(lambda article : getValueFor(article.category) == category, required_articles))
            query['category'] = category

        if tag:
            required_articles = list(filter(lambda article : article.has_tag(tag), required_articles))
            query['tag'] = tag

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
            "data" : {
                "page" : nested_model_to_dict(required_page),
                "page_range" : list(paginator.page_range()) if required_articles else None,
                "query" : list(query.items()),
                "hasResults" : (articles_count > 0)
            },
            "meta" : {
                "count" : articles_count
            }
        }

        return JsonResponse(content)


    @fail_safe_api(for_model=Article, needs_authentication=True)
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

        if (image):
            uploadImageFor(article, image, article.slug)

        tags = request.POST.get('tags', '').strip().split(",")

        setTagsFor(article, tags)

        article.save()

        content = {
            "status": 200,
            "message" : "article {}".format('drafted' if is_drafted else 'created'),
            "data": {
                "article": nested_model_to_dict(article),
            },
            "meta": {
                "count": 1,
            }
        }

        return JsonResponse(content)

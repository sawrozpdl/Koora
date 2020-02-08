from django.views import View
from articles.models import Article
from comments.models import Comment
from django.http import JsonResponse
from utils.decorators import fail_safe_api
from utils.models import nested_model_to_dict
from utils.request import parse_body, set_user
from utils.koora import deleteImageFor, generate_url_for, uploadImageFor, setTagsFor


class DetailAPIView(View):


    def dispatch(self, request, *args, **kwargs):
        set_user(request)
        if request.user.is_authenticated:
            parse_body(request, for_method=request.method)
        return super(DetailAPIView, self).dispatch(request, *args, **kwargs)


    @fail_safe_api(for_model=Article)
    def get(self, request, slug):

        article = Article.objects.get(slug=slug)

        content = {
            "status": 200,
            "data": {
                "article": nested_model_to_dict(article)
            },
            "meta": {
                "article_count": 1
            }
        }

        return JsonResponse(content)

    @fail_safe_api(for_model=Article, needs_authentication=True)
    def put(self, request, slug):

        article = Article.objects.get(slug=slug)        
        article.title = request.PUT.get('title', '')
        article.content = request.PUT.get('content', '')
        article.category = request.PUT.get('category', '')

        image = request.FILES.get('article_image', False)

        post_type = request.PUT.get('post_type', 'public')
        article.is_private = post_type == 'private'

        if image:
            deleteImageFor(article)
            uploadImageFor(article, image, article.slug)

        article.remove_tags()

        tags = request.PUT.get('tags', '').strip().split(",")

        setTagsFor(article, tags)

        article.save()

        return JsonResponse({
          "status" : 200,
          "data" : {
              "article" : nested_model_to_dict(article)
          },
          "message" : "article updated"
        })


    @fail_safe_api(for_model=Article, needs_authentication=True)
    def post(self, request, slug):
        article = Article.objects.get(slug=slug)

        user = request.user

        content = request.POST.get('content', '')
        object_id = request.POST.get('object_id', 1)
        content_type = article.content_type


        created_comment = Comment.objects.create(
            user=user, content=content, object_id=object_id, content_type=content_type)

        return JsonResponse({
            "status" : 200,
            "data" : nested_model_to_dict(created_comment),
            "message" : "comment added",
            "meta" : {
                "article_count" : 1,
                "comment_count" : 1
            }
        })



    @fail_safe_api(for_model=Article, needs_authentication=True)
    def delete(self, request, slug):

        article = Article.objects.get(slug=slug)

        if article.image_url:
            deleteImageFor(article)
        article.delete()

        return JsonResponse({
            "status" : 200,
            "message" : 'article deleted'
        })

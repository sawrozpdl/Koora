import json
from django.views import View
from articles.models import Article
from comments.models import Comment
from django.http import JsonResponse
from utils.request import parse_body, set_user
from utils.models import nested_model_to_dict
from utils.decorators import fail_safe_api
from utils.koora import deleteImageFor, generate_url_for, uploadImageFor, setTagsFor


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class DetailAPIView(View):


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            set_user(request)
        except Exception:
            return JsonResponse({
                'status' : 403
            })
        parse_body(request, for_method=request.method)
        return super(DetailAPIView, self).dispatch(request, *args, **kwargs)


    @fail_safe_api(for_model=Article)
    def get(self, request, slug):

        article = Article.objects.get(slug=slug)
        comments = article.comments

        content = {
            "status": 200,
            "data": {
                "article": nested_model_to_dict(article),
                "vote_type": article.get_user_vote(request.user)
            },
            "meta": {
                "article_count": 1,
                "comment_count": len(comments)
            }
        }

        return JsonResponse(content)

    @fail_safe_api(for_model=Article)
    def put(self, request, slug):

        article = Article.objects.get(slug=slug)        
        article.title = request.PUT.get('title', '')
        article.content = request.PUT.get('content', '')
        article.category = request.PUT.get('category', '')

        image = request.FILES.get('article_image', False)

        post_type = request.PUT.get('post_type', 'public')
        article.is_private = post_type == 'private'

        # if image:
        #     deleteImageFor(article)
        #     uploadImageFor(article, image, article.title)

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


    @fail_safe_api(for_model=Article)
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



    @fail_safe_api(for_model=Article)
    def delete(self, request, slug):

        article = Article.objects.get(slug=slug)

        # if article.image_url:
        #     deleteImageFor(article)
        article.delete()

        return JsonResponse({
            "status" : 200,
            "message" : 'article deleted'
        })

from django.views import View
from comments.models import Comment
from django.http import JsonResponse
from utils.decorators import fail_safe_api
from utils.models import nested_model_to_dict
from utils.request import parse_body, set_user
from django.contrib.contenttypes.models import ContentType


class DetailAPIView(View):

    def dispatch(self, request, *args, **kwargs):
        set_user(request)
        if request.user.is_authenticated:
            parse_body(request, for_method=request.method)
        return super(DetailAPIView, self).dispatch(request, *args, **kwargs)



    @fail_safe_api(for_model=Comment)
    def get(self, request, slug):

        comment = Comment.objects.get(slug=slug)

        comment_dict = nested_model_to_dict(comment)

        comment_dict['content_object'] = nested_model_to_dict(comment.content_object)

        content = {
            "status": 200,
            "data" : {
                "comment": comment_dict

            },
            "meta": {
                "count" : 1
            }
        }

        return JsonResponse(content)


    @fail_safe_api(for_model=Comment, needs_authentication=True)
    def post(self, request, slug):
        parent = Comment.objects.get(slug=slug)

        content_object = parent.content_object
        content_type = parent.content_type

        content = request.POST.get('content', '')

        object_id = content_object.id

        created_comment = Comment.objects.create(user=request.user, content=content,content_object=content_object,
                            content_type=content_type, parent=parent, object_id=object_id)

        content = {
            "status": 200,
            "data" : {
                "comment": nested_model_to_dict(created_comment)
            },
            "message" : 'created',
            "meta": {
                "count" : 1
            }
        }

        return JsonResponse(content)


    @fail_safe_api(for_model=Comment, needs_authentication=True)
    def delete(self, request, slug):

        comment = Comment.objects.get(slug=slug)

        is_parent = comment.is_parent

        parent = comment.content_object if is_parent else comment.parent

        comment.delete()

        content = {
            "status" : 200,
            "data" : {
                "is_parent" : is_parent,
                "parent_slug" : parent.slug,
            },
            "message" : "comment deleted"
        }

        return JsonResponse(content)


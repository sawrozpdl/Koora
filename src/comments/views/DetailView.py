from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType


class DetailView(View):

    def get(self, request, model, slug):
        comment = Comment.objects.get(slug=slug)
        template = loader.get_template("comments/comment_thread.html")
        content = {
            "page_name": model,
            "comment": comment
        }
        return HttpResponse(template.render(content, request))

    def post(self, request, model, slug):
        delete_mode = request.POST.get('delete_mode', False)
        if not delete_mode:
            parent = Comment.objects.get(slug=slug)
            content_object = parent.content_object
            content_type = parent.content_type
            content = request.POST.get('content', '')
            object_id = content_object.id
            Comment.objects.create(user=request.user, content=content,content_object=content_object,
                                content_type=content_type, parent=parent, object_id=object_id)
            template = loader.get_template("comments/comment_thread.html")
            content = {
                "page_name": model,
                "messages" : [
                    {
                        'type': 'success',
                        'content' : 'Reply Added!'
                    }
                ],
                "comment": parent
            }
            return HttpResponse(template.render(content, request))
        else:
            comment = Comment.objects.get(slug=slug)
            is_parent = comment.is_parent
            if comment.is_parent:
                content_object = comment.content_object
                comment.delete()
                content_name = model[:len(model) - 1]
                template = loader.get_template("{}/{}.html".format(model, content_name))
                content = {
                    "page_name": model,
                    content_name: content_object,
                    "vote_type" : content_object.get_user_vote(request.user),
                    "messages" : [
                        {
                            'type': 'success',
                            'content' : 'Comment Removed!'
                        }
                    ],
                    "comments" : content_object.comments
                }
                return HttpResponse(template.render(content, request))
            else:
                parent = comment.parent
                comment.delete()
                template = loader.get_template("comments/comment_thread.html")
                content = {
                    "page_name": model,
                    "messages" : [
                        {
                            'type': 'success',
                            'content' : 'Reply Removed!'
                        }
                    ],
                    "comment": parent
                }
                return HttpResponse(template.render(content, request))
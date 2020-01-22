from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from articles.models import Article
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType


class DetailView(View):

    def get(self, request, model, slug):
        comment = Comment.objects.get(slug=slug)
        template = loader.get_template("comments/comment_thread.html")
        content = {
            "page_name": "articles",
            "comment": comment
        }
        return HttpResponse(template.render(content, request))

    def post(self, request, model, slug):
        parent = Comment.objects.get(slug=slug)
        content_object = parent.content_object
        content_type = parent.content_type
        content = request.POST.get('content', '')
        object_id = content_object.id
        Comment.objects.create(user=request.user, content=content,content_object=content_object,
                               content_type=content_type, parent=parent, object_id=object_id)
        template = loader.get_template("comments/comment_thread.html")
        content = {
            "page_name": "articles",
            "messages" : [
                {
                    'type': 'success',
                    'content' : 'Reply Added!'
                }
            ],
            "comment": parent
        }
        return HttpResponse(template.render(content, request))

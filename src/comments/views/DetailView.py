from django.views import View
from django.template import loader
from comments.models import Comment
from utils.decorators import fail_safe
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from utils.koora import generate_url_for, get_message_or_default

class DetailView(View):

    @fail_safe(for_model=Comment)
    def get(self, request, model, slug):
        comment = Comment.objects.get(slug=slug)

        message = get_message_or_default(request, {})

        template = loader.get_template("comments/comment_thread.html")
        content = {
            "page_name": model,
            "comment": comment,
            "message" : message
        }
        return HttpResponse(template.render(content, request))


    @fail_safe(for_model=Comment)
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

            return HttpResponseRedirect(generate_url_for("comments:detail", kwargs={
                    "model" : model,
                    "slug" : slug
                }, query={
                    'type': 'success',
                    'content' : 'Reply Added!'
            }))

        else:

            comment = Comment.objects.get(slug=slug)
            is_parent = comment.is_parent

            if comment.is_parent:
                content_object = comment.content_object
                comment.delete()
                content_name = model[:len(model) - 1]

                return HttpResponseRedirect(generate_url_for("{}:detail".format(model), kwargs={
                    "slug" : content_object.slug
                }, query={
                    'type': 'success',
                    'content' : 'Comment Removed!'
                }))

            else:
                parent = comment.parent
                comment.delete()

                return HttpResponseRedirect(generate_url_for("comments:detail", kwargs={
                    "model" : model,
                    "slug" : parent.slug
                }, query={
                    'type': 'success',
                    'content' : 'Reply Removed!'
                }))
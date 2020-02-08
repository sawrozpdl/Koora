from django.views import View
from django.template import loader
from utils.request import api_call, suitableRedirect
from comments.models import Comment
from utils.decorators import protected_view
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.contrib.contenttypes.models import ContentType
from utils.koora import generate_url_for, get_message_or_default

class DetailView(View):

    def get(self, request, model, slug):

        raw_response = api_call(
            method='get',
            request=request,
            reverse_for="comments-api:detail",
            reverse_kwargs={'slug' : slug}
        )

        response = raw_response.json()


        message = get_message_or_default(request, {})

        template = loader.get_template("comments/comment_thread.html")

        if response['status'] == 200:
            content = {
                "page_name": model,
                "comment": response['data']['comment'],
                "message" : message
            }
            return HttpResponse(template.render(content, request))
        else:
            return suitableRedirect(response=raw_response, reverse_name="comments:detail", reverse_kwargs={
                "slug" : slug,
                "model" : model
            })



    @protected_view(allow='logged_users', fallback='accounts/login.html', message="You don't have access to the page")
    def post(self, request, model, slug):

        delete_mode = request.POST.get('delete_mode', False)

        if not delete_mode:

            response = api_call(
                method='post',
                request=request,
                reverse_for="comments-api:detail",
                reverse_kwargs={'slug' : slug},
                data=request.POST.dict()
            ).json()

            if response['status'] == 200:
                return HttpResponseRedirect(generate_url_for("comments:detail", kwargs={
                        "model" : model,
                        "slug" : slug
                    }, query={
                        'type': 'success',
                        'content' : 'Reply Added!'
                }))
            else:
                return suitableRedirect(response=response, reverse_name="comments:detail", reverse_kwargs={
                    "slug" : slug,
                    "model" : model
                })


        else:

            response = api_call(
                method='delete',
                request=request,
                reverse_for="comments-api:detail",
                reverse_kwargs={'slug' : slug}
            ).json()

            togo = model

            if response['status'] == 200:
                kwargs = {
                    'slug' : response['data']['parent_slug']
                }
                query = {
                    'type': 'success',
                    'content' : 'Comment Removed!'
                }
                if not response['data']['is_parent']:
                    togo = "comments"
                    kwargs['model'] = model
                    query = {
                        'type': 'success',
                        'content' : 'Reply Removed!'
                    }
                return HttpResponseRedirect(generate_url_for("{}:detail".format(togo), kwargs=kwargs, query=query))
            else:
                return suitableRedirect(response=response, reverse_name="comments:detail", reverse_kwargs={
                    "slug" : slug,
                    "model" : model
                })


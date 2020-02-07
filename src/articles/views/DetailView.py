import requests
from django.views import View
from django.template import loader
from utils.koora import get_message_or_default, generate_url_for
from utils.decorators import protected_view
from utils.request import api_call
from django.http import HttpResponse, HttpResponseRedirect


class DetailView(View):

    def get(self, request, slug):

        response = api_call(
            method='get',
            request=request,
            reverse_for="articles-api:detail",
            reverse_kwargs={'slug' : slug}
        ).json()

        message = get_message_or_default(request, {})

        if response['status'] == 200:
            article = response['data']['article']
            template = loader.get_template("articles/article.html")
            content = {
                "page_name": "articles",
                "article": article,
                "message" : message,
                "vote_type" : response['data']['vote_type'],
                "comments" : article['comments']
            }
            return HttpResponse(template.render(content, request))
        else:
            return HttpResponseRedirect(generate_url_for("articles:detail", kwargs={
                "slug" : slug
            }, query={
                "type" : "danger",
                "content" : response['message']
            }))


    @protected_view(allow='logged_users', fallback='accounts/login.html', message="Login to post/delete contents")
    def post(self, request, slug):

        deleteMode = request.POST.get('deletemode', False)


        if deleteMode:

            response = api_call(
                method='delete',
                request=request,
                reverse_for="articles-api:detail",
                reverse_kwargs={'slug' : slug}
            ).json()
            

            if response['status'] == 200:
                return HttpResponseRedirect(generate_url_for("articles:list", query={
                    "type" : "success",
                    "content" : "Article deletion successful!"
                }))
            else :
                return HttpResponseRedirect(generate_url_for("articles:detail", query={
                    "type" : "danger",
                    "content" : response['message']
                }))

        else:

            response = api_call(
                method='post',
                request=request,
                reverse_for="articles-api:detail",
                reverse_kwargs={'slug' : slug},
                data=request.POST.dict()
            ).json()

            if response['status'] == 200:
                return HttpResponseRedirect(generate_url_for("articles:detail", kwargs={
                    "slug" : slug
                }, query={
                    "type" : "success",
                    "content" : "Comment Added!"
                }))
            else:
                return HttpResponseRedirect(generate_url_for("articles:detail",kwargs={
                    "slug" : slug
                }, query={
                    "type" : "danger",
                    "content" : response['message']
                }))

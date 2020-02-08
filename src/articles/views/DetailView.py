import requests
from django.views import View
from django.template import loader
from utils.request import api_call, suitableRedirect
from utils.request import suitableRedirect
from utils.decorators import protected_view
from django.http import HttpResponse, HttpResponseRedirect
from utils.koora import get_message_or_default, generate_url_for


class DetailView(View):

    def get(self, request, slug):

        raw_response = api_call(
            method='get',
            request=request,
            reverse_for="articles-api:detail",
            reverse_kwargs={'slug' : slug}
        )

        response = raw_response.json()


        message = get_message_or_default(request, {})

        if response['status'] == 200:
            article = response['data']['article']
            template = loader.get_template("articles/article.html")
            content = {
                "page_name": "articles",
                "article": article,
                "message" : message,
                "comments" : article['comments']
            }
            return HttpResponse(template.render(content, request))
        else:
            return suitableRedirect(response=raw_response, reverse_name="articles:detail", reverse_kwargs={
                "slug" : slug
            })



    @protected_view(allow='logged_users', fallback='accounts/login.html', message="Login to post/delete contents")
    def post(self, request, slug):

        deleteMode = request.POST.get('deletemode', False)


        if deleteMode:

            raw_response = api_call(
                method='delete',
                request=request,
                reverse_for="articles-api:detail",
                reverse_kwargs={'slug' : slug}
            )

            response = raw_response.json() 

            if response['status'] == 200:
                return HttpResponseRedirect(generate_url_for("articles:list", query={
                    "type" : "success",
                    "content" : "Article deletion successful!"
                }))
            else :
                return suitableRedirect(response=raw_response, reverse_name="articles:list")

        else:

            raw_response = api_call(
                method='post',
                request=request,
                reverse_for="articles-api:detail",
                reverse_kwargs={'slug' : slug},
                data=request.POST.dict()
            )

            response = raw_response.json()

            if response['status'] == 200:
                return HttpResponseRedirect(generate_url_for("articles:detail", kwargs={
                    "slug" : slug
                }, query={
                    "type" : "success",
                    "content" : "Comment Added!"
                }))
            else:
                return suitableRedirect(response=raw_response, reverse_name="articles:detail", reverse_kwargs={
                    "slug" : slug
                })

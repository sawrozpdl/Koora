from django.views import View
from django.urls import reverse
from django.conf import settings
from django.template import loader
from articles.models import Article
from utils.decorators import protected_view
from utils.request import api_call, suitableRedirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from utils.koora import setTagsFor, uploadImageFor, deleteImageFor, get_message_or_default, generate_url_for
class UpdateView(View):

    def get(self, request, slug):

        raw_response = api_call(
            method='get',
            request=request,
            reverse_for="articles-api:detail",
            reverse_kwargs={'slug' : slug}
        )

        response = raw_response.json()


        message = get_message_or_default(request, {
            "type" : "warning",
            "content" : "Change required field and Press Update to Publish the new verson of your Article"
        })

        if response['status'] == 200:
            return HttpResponse(loader.get_template('articles/post_article.html').render({
                "page_name": "articles",
                "message" : message,
                "article" : response['data']['article'],
                "update_mode" : True,
                "tags" : response['data']['article']['tag_string']
            }, request))
        else:
            return suitableRedirect(response=raw_response, reverse_name="articles:update", reverse_kwargs={
                "slug" : slug
            })


    @protected_view(allow='logged_users', fallback='accounts/login.html', message="You don't have access to the page")
    def post(self, request, slug):

        raw_response = api_call(
            method='put',
            request=request,
            reverse_for="articles-api:detail",
            reverse_kwargs={'slug' : slug},
            data = request.POST.dict(),
            files = request.FILES.dict()
        )

        response = raw_response.json()


        if response['status'] == 200:
            return HttpResponseRedirect(response['data']['article']['absolute_url'])
        else:
            return suitableRedirect(response=raw_response, reverse_name="articles:update", reverse_kwargs={
                "slug" : slug
            })
    
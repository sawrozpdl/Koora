import requests
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.template import loader
from articles.models import Article
from utils.decorators import fail_safe, protected_view
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from utils.koora import setTagsFor, uploadImageFor, deleteImageFor, get_message_or_default, generate_url_for
class UpdateView(View):

    #@fail_safe(for_model=Article)
    def get(self, request, slug):

        headers = {
            'X-CSRFToken' : request.POST.get('csrfmiddlewaretoken', ''),
            'Token' : str(request.user.id)
        }

        response = requests.get(url = request.build_absolute_uri(generate_url_for('articles-api:detail', kwargs={'slug' : slug})), headers=headers,  verify=False)
        
        response = response.json()

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
            return HttHttpResponseServerError()


    #@fail_safe(for_model=Article)
    @protected_view(allow='logged_users', fallback='accounts/login.html', message="You don't have access to the page")
    def post(self, request, slug):

        headers = {
            'X-CSRFToken' : request.POST.get('csrfmiddlewaretoken', ''),
            'Token' : str(request.user.id)
        }

        data = request.POST.dict()
        image = request.FILES.dict()

        response = requests.put(url = request.build_absolute_uri(generate_url_for('articles-api:detail', kwargs={'slug' : slug})), data=data, files=image, headers=headers,  verify=False)
        
        response = response.json()

        if response['status'] == 200:
            return HttpResponseRedirect(response['data']['article']['absolute_url'])
        else:
            return HttpResponseRedirect(generate_url_for('articles:update'), kwargs={slug : slug}, query = {
                "type" : "danger",
                "content" : response['message']
            })
    
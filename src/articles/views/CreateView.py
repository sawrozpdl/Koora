import json
import requests
from django.views import View
from django.conf import settings
from django.template import loader
from articles.models import Article
from utils.decorators import protected_view, fail_safe
from django.http import HttpResponse, HttpResponseRedirect
from utils.koora import setTagsFor, uploadImageFor, get_message_or_default, generate_url_for

class CreateView(View):

    def get(self, request):

        message = get_message_or_default(request, {
            "type" : "warning",
            "content" : "Fill up your article and Click Post to publish and Draft to save it as a Draft"
        })

        return HttpResponse(loader.get_template('articles/post_article.html').render({
            "page_name" : "create_article",
            "message" : message
        }, request))


    #@fail_safe(for_model=Article)
    @protected_view(allow='logged_users', fallback='accounts/login.html', message="You need to be logged in to create an article")
    def post(self, request):

        headers = {
            'X-CSRFToken' : request.POST.get('csrfmiddlewaretoken', ''),
            'Token' : str(request.user.id)
        }

        data = request.POST.dict()
        image = request.FILES.dict()

        response = requests.post(url = request.build_absolute_uri(generate_url_for('articles-api:list')), data=data, files=image, headers=headers,  verify=False)
        
        response = response.json()

        if response['status'] == 200:
            if response['data']['article']['is_drafted']:
                return HttpResponseRedirect(generate_url_for('articles:create', query = {
                    "type" : "success",
                    "content" : "Article Drafted, to publish it, go to your profile"
                }))
            else:
                return HttpResponseRedirect(response['data']['absolute_url'])
        else:
            return HttpResponseRedirect(generate_url_for('articles:create', query = {
                    "type" : "danger",
                    "content" : response['message']
                }))
        
        
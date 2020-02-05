import requests
from django.views import View
from django.template import loader
from django.http import HttpResponse, HttpResponseServerError
from utils.koora import get_message_or_default
from utils.decorators import fail_safe
from utils.koora import generate_url_for

class ListView(View):

    def get(self, request):

        headers = {
            'X-CSRFToken' : request.POST.get('csrfmiddlewaretoken', ''),
            'Token' : str(request.user.id)
        }

        params = request.GET.dict()

        response = requests.get(url = request.build_absolute_uri(generate_url_for('articles-api:list')), params=params, headers=headers,  verify=False)
        
        response = response.json()

        message = get_message_or_default(request, {})

        template = loader.get_template('articles/articles.html')

        if response['status'] == 200:
            content = {
                "page_name": "articles",
                "message" : message,
                "page" : response['data']['page'],
                "page_range" : response['data']['page_range'],
                "query" : response['data']['query'],
                "hasResults" : response['data']['hasResults']
            }

            return HttpResponse(template.render(content, request))
        else:
            return HttpResponseServerError()
            
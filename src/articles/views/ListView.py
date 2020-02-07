from django.views import View
from django.template import loader
from utils.request import api_call
from utils.koora import get_message_or_default
from django.http import HttpResponse, HttpResponseServerError
class ListView(View):

    def get(self, request):

        params = request.GET.dict()

        response = api_call(
            method='get',
            request=request,
            reverse_for="articles-api:list",
            reverse_params=params,
            data = request.GET.dict()
        ).json()

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
            return suitableRedirect(response=response, reverse_name="articles:list")
            
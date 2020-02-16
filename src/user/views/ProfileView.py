from user.models import User
from django.views import View
from django.template import loader
from django.http import HttpResponse
from utils.koora import get_message_or_default
from utils.request import api_call


class ProfileView(View):

    def get(self, request, username=None):

        message = get_message_or_default(request, {})

        user = User.objects.get(username=username) if username else request.user

        content = {
          "page_name": "profile",
          "message": message,
          "user" : user
        }

        params = request.GET.dict()

        params['atype'] = "public"
        params['size'] = 3

        if username:
            params['uid'] = user.id

        raw_response = api_call(
            method='get',
            request=request,
            reverse_for="articles-api:list",
            reverse_params=params,
        )

        response = raw_response.json()

        if response['status'] == 200:
            content = {
                **content,
                "page" : response['data']['page'],
                "page_range" : response['data']['page_range'],
                "query" : response['data']['query'],
                "hasResults" : response['data']['hasResults']
            }


        return HttpResponse(loader.get_template('user/profile.html').render(content, request))
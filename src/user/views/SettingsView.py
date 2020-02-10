from user.models import User
from django.views import View
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from utils.koora import get_message_or_default, generate_url_for


class SettingsView(View):

    def get(self, request):

        message = get_message_or_default(request, {})

        return HttpResponse(loader.get_template('user/settings.html').render({
            "page_name": "settings",
            "message": message
        }, request))



    def post(self, request):

        print('got : ', request.POST.dict())

        query = {}

        if request.POST.get("profile_update", False):
          query = self.handle_profile_update(request)

        elif request.POST.get("account_update", False):
          query = self.handle_account_update(request)

        elif request.POST.get("social_update", False):
          query = self.handle_social_update(request)

        elif request.POST.get("password_update", False):
          query = self.handle_password_update(request)

        elif request.POST.get("billing_update", False):
          query = self.handle_billing_update(request)


        return HttpResponseRedirect(generate_url_for("user:settings", query=query))




    def handle_profile_update(self, request):
      return {
        'type' : 'success',
        'content' : 'Successfully updated the profile!'
      }

    def handle_account_update(self, request):
      return {
        'type' : 'success',
        'content' : 'Successfully updated the account!!'
      }

    def handle_social_update(self, request):
      return {
        'type' : 'success',
        'content' : 'Successfully updated social accounts!!'
      }

    def handle_password_update(self, request):
      return {
        'type' : 'success',
        'content' : 'Successfully updated passwords!'
      }

    def handle_billing_update(self, request):
      return {
        'type' : 'success',
        'content' : 'updated!'
      }


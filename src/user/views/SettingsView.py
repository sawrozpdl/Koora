from user.models import User
from django.views import View
from django.template import loader
from django.http import HttpResponse
from utils.koora import get_message_or_default, generate_url_for


class SettingsView(View):

    def get(self, request, username):

        message = get_message_or_default(request, {})

        return HttpResponse(loader.get_template('user/settings.html').render({
            "page_name": "settings",
            "message": message
        }, request))



    def post(self, request, username):

        query = {}

        if request.POST.get("profile_update"):
          query = self.handle_profile_update(request, username)

        elif request.POST.get("account_update"):
          query = self.handle_account_update(request, username)

        elif request.POST.get("social_update"):
          query = self.handle_social_update(request, username)

        elif request.POST.get("password_update"):
          query = self.handle_password_update(request, username)

        elif request.POST.get("billing_update"):
          query = self.handle_billing_update(request, username)


        return HttpResponseRedirect(generate_url_for("user:settings", query))




    def handle_profile_update(self, request, username):
      return {
        'type' : 'success',
        'content' : 'updated!'
      }

    def handle_account_update(self, request, username):
      return {
        'type' : 'success',
        'content' : 'updated!'
      }

    def handle_social_update(self, request, username):
      return {
        'type' : 'success',
        'content' : 'updated!'
      }

    def handle_password_update(self, request, username):
      return {
        'type' : 'success',
        'content' : 'updated!'
      }

    def handle_billing_update(self, request, username):
      return {
        'type' : 'success',
        'content' : 'updated!'
      }


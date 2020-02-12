import jwt
from django.views import View
from django.conf import settings
from django.template import loader
from utils.koora import generate_url_for
from django.contrib.auth.models import User
from utils.decorators import for_unauthenticated
from django.http import HttpResponse, HttpResponseRedirect
 
class ChangePasswordView(View):

    @for_unauthenticated
    def get(self, request):

        token = request.GET.get('t', None)

        if not token:
            return HttpResponseRedirect(generate_url_for('accounts:login', query={
                'type': 'danger',
                'content': 'You were not allowed to be there!'
            }))

        payload = None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        except:
            return HttpResponseRedirect(generate_url_for('accounts:login', query={
                'type': 'danger',
                'content': 'The password reset link has expired or is invalid!'
            }))


        user_id = payload['user_id']
        user_email = payload['email']

        if not user_id:
            return HttpResponseRedirect(generate_url_for('accounts:login', query={
                'type': 'danger',
                'content': "There's no account associated with email : {}".format(user_email)
            }))

        return HttpResponse(loader.get_template('accounts/change_password.html').render({
            'user_id' : user_id,
            "message": {
              'type' : 'success',
              'content' : 'Verification Successfull! You may now set a new password!'
            }
        }, request))


    @for_unauthenticated
    def post(self, request):

        user_id = request.POST.get('user_id', None)

        user = User.objects.get(id=user_id)

        new_password = request.POST.get('password', 1)
        confirm_password = request.POST.get('password_repeat', 2)

        if new_password != confirm_password:
            return HttpResponseRedirect(generate_url_for("accounts/change_password.html", query={
                "type": "danger",
                "content": "Password doesn't match"
            }))


        user.set_password(new_password)

        user.save()

        return HttpResponseRedirect(generate_url_for('accounts:login', query={
          'type' : 'success',
          'content' : 'Password changed, You may now log in!'
        }))

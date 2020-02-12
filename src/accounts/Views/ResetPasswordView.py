import jwt
import platform
from django.contrib.auth.models import User
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta
from utils.request import generate_url_for
from django.http import HttpResponseRedirect, Http404
from utils.decorators import for_unauthenticated
from django.template.loader import render_to_string


class ResetPasswordView(View):


    def get(self, request):
        raise Http404()

    @for_unauthenticated
    def post(self, request):

        from_email = 'Koora <no-reply@kooora.herokuapp.com>'

        to_email = request.POST.get('email', '')

        user = None

        try:
                user = User.objects.get(email=to_email)
        except:
                pass

        payload = {
            'user_id': user.id if user else None,
            'email' : to_email,
            'exp': datetime.utcnow() + timedelta(seconds=(settings.JWT_EXP_DELTA_SECONDS / 6))
        }

        accessToken = jwt.encode(
            payload, settings.SECRET_KEY, settings.JWT_ALGORITHM).decode('utf-8')

        reset_url = request.build_absolute_uri(generate_url_for('accounts:forgot', query={
                't' : accessToken
        }))

        html_message = render_to_string(
            'accounts/email_forgot_password.html', {
                'username': user.username if user else 'Mr. Visitor',
                'action_url': reset_url,
                'homepage': request.build_absolute_uri(generate_url_for('home')),
                'operating_system': '{} {}'.format(platform.system(), platform.release()),
                'browser_name': request.META['HTTP_USER_AGENT']
            })

        send_mail('Forgot Password?',
                  'Here is where you make things right again!',
                  from_email,
                  [to_email],
                  html_message=html_message
                  )

        return HttpResponseRedirect(generate_url_for('accounts:login', query={
            'type': 'success',
            'content': 'Verification mail sent to {}, follow the instructions there to reset your password!'.format(to_email)
        }))

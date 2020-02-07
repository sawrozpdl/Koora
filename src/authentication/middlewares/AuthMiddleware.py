import jwt
from django.conf import settings
from datetime import datetime, timedelta

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXP_DELTA_SECONDS = settings.JWT_EXP_DELTA_SECONDS
COOKIE_MAX_AGE = 365 * 24 * 60 * 60  

class AuthMiddleware(object):

    def __init__(self, get_response):

        self.get_response = get_response


    def __call__(self, request):

        print('you are : ', request.user)
        
        accessToken = request.COOKIES.get('accessToken', None) 
        if accessToken: # continue with the token
            print('old one here')
            request.META['Token'] = accessToken
            return self.get_response(request)


        if request.user.is_authenticated: # login backend
            print('you are all set in ')
            payload = {
                'user_id': request.user.id,
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            accessToken = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM).decode('utf-8')

            max_age = COOKIE_MAX_AGE
            expires = datetime.now() + timedelta(seconds=max_age)

            response = self.get_response(request)

            response.set_cookie('accessToken', accessToken, expires=expires.utctimetuple())

            return response

          # logout backend
        print('wait thats illegal')
        return self.get_response(request)
        # request.META['Token'] = None
        # response = self.get_response(request)
        # response.delete_cookie('accessToken')
        # return response
            
            
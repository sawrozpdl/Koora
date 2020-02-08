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


        if request.user.is_authenticated:

            aToken = request.COOKIES.get('accessToken', '')

            try:
                jwt.decode(aToken, JWT_SECRET, JWT_ALGORITHM)
            except Exception:
                
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

        elif not request.user.is_authenticated and 'accessToken' in request.COOKIES.keys(): 

            response = self.get_response(request)
            response.delete_cookie('accessToken')
            return response

        return self.get_response(request)

            
            
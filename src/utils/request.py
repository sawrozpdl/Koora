import jwt
import requests
from django.conf import settings
from utils.koora import generate_url_for
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser 
from django.http import HttpResponseRedirect, Http404


JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXP_DELTA_SECONDS = settings.JWT_EXP_DELTA_SECONDS



def parse_body(request, for_method="PUT"):

    if (request.method == "POST"):
        return

    # set post temporarily to access _load_post_and_files method
    request.method = "POST"

    request._load_post_and_files()
    request.method = for_method

    if for_method == 'PUT':
        request.PUT = request.POST

    elif for_method == 'PATCH':
        request.PATCH = request.POST

    elif for_method == 'DELETE':
        request.DELETE = request.POST



def set_user(request):

    active_user = AnonymousUser()

    try:
        access_token = request.COOKIES.get('accessToken', request.headers.get('Token', None))
        decoded = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        active_user = User.objects.get(id=decoded['user_id'])
    except Exception:
        pass

    request.user = active_user




def api_call(*args, **kwargs):

    request = kwargs['request']

    csrftoken = kwargs['request'].POST.get('csrfmiddlewaretoken', '')

    headers = {
        'X-CSRFToken' : csrftoken,
        'Token' : request.headers.get('Token', None)
    }

    cookies = {
        'csrftoken' : csrftoken,
        'accessToken' : request.COOKIES.get('accessToken', None) 
    }

    reverse_kwargs = kwargs.get('reverse_kwargs', None)
    reverse_params = kwargs.get('reverse_params', None)
    reverse_for = kwargs.get('reverse_for', '')

    data = kwargs.get('data', None)
    files = kwargs.get('files', None)
    
    return getattr(requests, kwargs.get('method', 'get'))(url = request.build_absolute_uri(generate_url_for(reverse_for, kwargs=reverse_kwargs, query=reverse_params)), headers=headers, cookies=cookies, data=data, files=files)



def suitableRedirect(*args, **kwargs):

    raw_response = kwargs.get('response', None)
    reverse_kwargs = kwargs.get('reverse_kwargs', None)
    reverse_name = kwargs.get('reverse_name', None)

    response = raw_response.json()

    togo = reverse_name
    message = response['message']

    query={
        "type" : "danger",
        "content" : message
    }


    if not response or response['status'] == 404:
        return Http404()
        
    elif response['status'] == 403:
        togo = "auth-api:logout"
        message = "Please login to continue"
        reverse_kwargs = None
        query['next'] = response['from']


    return HttpResponseRedirect(generate_url_for(togo, kwargs=reverse_kwargs, query=query))



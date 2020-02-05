from django.contrib.auth.models import User



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
    user_id = request.headers['Token']
    request.user = User.objects.get(id=user_id)

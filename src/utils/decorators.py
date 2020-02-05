import json
from django.template import loader
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseForbidden, HttpResponseServerError


def protected_view(*main_args, **main_kwargs):
    def protected_view_decorator(callback):
        def wrapper(*args, **kwargs):
            if args[1].user.is_authenticated:
                return callback(*args, **kwargs)
            else:
                content = {
                    "message": {
                        "type": "warning",
                        "content": main_kwargs['message'] or 'You dont have permission for that!'
                    },
                }
                return HttpResponse(loader.get_template(main_kwargs['fallback']).render(content, args[1]))
        return wrapper
    return protected_view_decorator


def protected_view_api(*main_args, **main_kwargs):
    def protected_view_decorator(callback):
        def wrapper(*args, **kwargs):
            request_body = json.loads(args[1].body)
            if request_body.user.is_authenticated:
                return callback(*args, **kwargs)
            else:
                content = {
                    "status" : 403,
                    "data" : 'unauthorized',
                    "meta" : {}
                }
                return JsonResponse(content)
        return wrapper
    return protected_view_decorator


def fail_safe(*main_args, **main_kwargs):
    def fail_safe_decorator(callback):
        def wrapper(*args, **kwargs):
            try:
                response = callback(*args, **kwargs)
            except:
                raise Http404('Such {} not found'.format(
                    main_kwargs['for_model'].__class__.__name__))
            return response
        return wrapper
    return fail_safe_decorator


def fail_safe_api(*main_args, **main_kwargs):
    def fail_safe_decorator(callback):
        def wrapper(*args, **kwargs):
            try:
                response = callback(*args, **kwargs)
            except:
                content = {
                    "status" : 404,
                    "data" : 'not found',
                    "meta" : {}
                }
                response = JsonResponse(content)
            return response
        return wrapper
    return fail_safe_decorator
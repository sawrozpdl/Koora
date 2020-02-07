import json
from django.template import loader
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, SuspiciousOperation

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


def fail_safe_api(*main_args, **main_kwargs):
    def fail_safe_decorator(callback):
        def wrapper(*args, **kwargs):

            request = args[1]
            
            if main_kwargs.get('needs_authentication', False) and not request.user.is_authenticated:
                return JsonResponse({
                    "status" : 403,
                    "message" : 'Not authorized',
                    "from" : request.path.replace('/api', '')
                })

            try:

                response = callback(*args, **kwargs)

            except ObjectDoesNotExist:

                content = {
                    "status" : 404,
                    "message" : 'Not found'
                }
                return JsonResponse(content)

            except (MultipleObjectsReturned, SuspiciousOperation):

                content = {
                    "status" : 400,
                    "message" : 'Invalid Operation'
                }
                return JsonResponse(content)

            except Exception:

                content = {
                    "status" : 500,
                    "message" : 'Internal Server Error'
                }
                return JsonResponse(content)

            return response

        return wrapper
        
    return fail_safe_decorator

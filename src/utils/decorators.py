from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError


def protected_view(*main_args, **main_kwargs):
    def protected_view_decorator(callback):
        def wrapper(*args, **kwargs):
            if args[0]["user"]["is_authenticated"]:
                return callback(*args, **kwargs)
            else:
                content = {
                    "messages": [
                        {
                            "type": "warning",
                            "content": main_kwargs['message']
                        }
                    ],
                }
                return HttpResponse(loader.get_template(main_kwargs['fallback']).render(content, args[0]))
        return wrapper
    return protected_view_decorator


def fail_safe(*main_args, **main_kwargs):
    def fail_safe_decorator(callback):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except main_kwargs['for'].DoesNotExist:
                raise Http404()
            except:
                return HttpResponseServerError()
        return wrapper
    return fail_safe_decorator

import requests
from django.views import View
from django.template import loader
from comments.models import Comment
from utils.decorators import fail_safe
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.contrib.contenttypes.models import ContentType
from utils.koora import generate_url_for, get_message_or_default

class DetailView(View):

    #@fail_safe(for_model=Comment)
    def get(self, request, model, slug):

        headers = {
            'X-CSRFToken' : request.POST.get('csrfmiddlewaretoken', ''),
            'Token' : str(request.user.id)
        }

        response = requests.get(url = request.build_absolute_uri(generate_url_for('comments-api:detail', kwargs={'slug' : slug})), headers=headers,  verify=False)
        
        response = response.json()

        message = get_message_or_default(request, {})

        template = loader.get_template("comments/comment_thread.html")

        if response['status'] == 200:
            content = {
                "page_name": model,
                "comment": response['data']['comment'],
                "message" : message
            }
            return HttpResponse(template.render(content, request))
        else:
            return HttpResponseServerError()


    #@fail_safe(for_model=Comment)
    def post(self, request, model, slug):

        delete_mode = request.POST.get('delete_mode', False)

        headers = {
            'X-CSRFToken' : request.POST.get('csrfmiddlewaretoken', ''),
            'Token' : str(request.user.id)
        }

        if not delete_mode:

            data = request.POST.dict()

            response = requests.post(url = request.build_absolute_uri(generate_url_for('comments-api:detail', kwargs={'slug' : slug})), headers=headers, data=data,  verify=False)
        
            response = response.json()


            if response['status'] == 200:
                return HttpResponseRedirect(generate_url_for("comments:detail", kwargs={
                        "model" : model,
                        "slug" : slug
                    }, query={
                        'type': 'success',
                        'content' : 'Reply Added!'
                }))
            else:
                return HttpResponseServerError()


        else:

            response = requests.delete(url = request.build_absolute_uri(generate_url_for('comments-api:detail', kwargs={'slug' : slug})), headers=headers,  verify=False)
        
            response = response.json()

            togo = model

            if response['status'] == 200:
                kwargs = {
                    'slug' : response['data']['parent_slug']
                }
                query = {
                    'type': 'success',
                    'content' : 'Comment Removed!'
                }
                if not response['data']['is_parent']:
                    togo = "comments"
                    kwargs['model'] = model
                    query = {
                        'type': 'success',
                        'content' : 'Reply Removed!'
                    }
                print('fjdk',togo, kwargs)
                return HttpResponseRedirect(generate_url_for("{}:detail".format(togo), kwargs=kwargs, query=query))
            else:
                return HttpResponseServerError()

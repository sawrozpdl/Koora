import requests
from django.views import View
from django.template import loader
from utils.koora import get_message_or_default, generate_url_for
from utils.decorators import fail_safe, protected_view
from django.http import HttpResponse, HttpResponseRedirect

class DetailView(View):

    #@fail_safe(for_model=Article)
    def get(self, request, slug):

        headers = {
            'X-CSRFToken' : request.POST.get('csrfmiddlewaretoken', ''),
            'Token' : str(request.user.id)
        }

        response = requests.get(url = request.build_absolute_uri(generate_url_for('articles-api:detail', kwargs={'slug' : slug})), headers=headers,  verify=False)
        
        response = response.json()

        message = get_message_or_default(request, {})

        if response['status'] == 200:
            article = response['data']['article']
            template = loader.get_template("articles/article.html")
            content = {
                "page_name": "articles",
                "article": article,
                "message" : message,
                "vote_type" : response['data']['vote_type'],
                "comments" : article['comments']
            }
            return HttpResponse(template.render(content, request))
        else:
            return HttpResponseRedirect(generate_url_for("articles:detail", kwargs={
                "slug" : slug
            }, query={
                "type" : "danger",
                "content" : response['message']
            }))


    @protected_view(allow='logged_users', fallback='accounts/login.html', message="Login to post/delete contents")
    def post(self, request, slug):

        deleteMode = request.POST.get('deletemode', False)


        headers = {
            'X-CSRFToken' : request.POST.get('csrfmiddlewaretoken', ''),
            'Token' : str(request.user.id)
        }

        if deleteMode:
            
            response = requests.delete(url = request.build_absolute_uri(generate_url_for('articles-api:detail', kwargs={'slug' : slug})), headers=headers,  verify=False)
        
            response = response.json()

            if response['status'] == 200:
                return HttpResponseRedirect(generate_url_for("articles:list", query={
                    "type" : "success",
                    "content" : "Article deletion successful!"
                }))
            else :
                return HttpResponseRedirect(generate_url_for("articles:detail", query={
                    "type" : "danger",
                    "content" : response['message']
                }))

        else:

            headers = {
                'X-CSRFToken' : request.POST.get('csrfmiddlewaretoken', ''),
                'Token' : str(request.user.id)
            }

            data = request.POST.dict()

            response = requests.post(url = request.build_absolute_uri(generate_url_for('articles-api:detail', kwargs={'slug' : slug})), data=data, headers=headers,  verify=False)
            
            response = response.json()

            if response['status'] == 200:
                return HttpResponseRedirect(generate_url_for("articles:detail", kwargs={
                    "slug" : slug
                }, query={
                    "type" : "success",
                    "content" : "Comment Added!"
                }))
            else:
                return HttpResponseRedirect(generate_url_for("articles:detail",kwargs={
                    "slug" : slug
                }, query={
                    "type" : "danger",
                    "content" : response['message']
                }))

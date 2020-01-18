from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from articles.models import Article

class DetailView(View):

    def get(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
            template = loader.get_template("articles/article.html")
            content = {
                "page_name": "articles",
                "article": article
            }
            return HttpResponse(template.render(content, request))
        except Article.DoesNotExist:
            raise Http404()
        except:
            return HttpResponseServerError()

    def post(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
            article.delete()
            articles = Article.objects.all()
            template = loader.get_template("articles/articles.html")
            content = {
                "page_name": "articles",
                "messages" : [
                    {
                        "type" : "success",
                        "content" : "Article deletion successful!"
                    }
                ],
                "title" : "Articles by Users:",
                "articles" : articles
            }
            return HttpResponse(template.render(content, request))
        except Article.DoesNotExist:
            raise Http404()
        except:
            return HttpResponseServerError()
        

from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from articles.models import Article
from articles.models import Tag
from django.conf import settings
from utils import uploader


class CreateView(View):

    def get(self, request):
        return HttpResponse(loader.get_template('articles/create_article.html').render({
            "page_name" : "create_article",
            "messages" : [
                {
                    "type" : "warning",
                    "content" : "Fill up your article and Click Post to publish and Draft to save it as a Draft"
                }
            ]
        }, request))

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden() # redirect to login 
        try:
            title = request.POST['title']
            content = request.POST['content']
            category = request.POST['category']
            image = request.FILES.get('article_image', False)
            image_url = ''
            if (image):
                key = "%s_%s.jpg" % (request.user.username, title)
                image_url = uploader.upload(image, key)
            article = Article.objects.create(title=title, content=content, category=category, image_url=image_url)
            tags = request.POST.get('tags', '').split(", ")
            if len(tags) > 0:
                for tag in tags:
                    try:
                        existing_tag = Tag.objects.get(name=tag)
                        article.tags.add(existing_tag)
                    except:
                        article.tags.create(name=tag, description='nonefeornow')
                article.save()
            return HttpResponse(loader.get_template("articles/create_article.html").render({
                "page_name" : "create_article",
                "messages" : [
                    {
                        "type" : "success",
                        "content" : "Article creation successful!"
                    }
                ]
            }, request))
        except:
            return HttpResponseServerError()
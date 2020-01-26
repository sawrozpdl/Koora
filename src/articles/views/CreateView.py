from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from articles.models import Article
from articles.models import Tag
from django.conf import settings
from utils import uploader
from datetime import datetime
from utils.decorators import protected_view, fail_safe
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


    @fail_safe(for_model=Article)
    @protected_view(allow='logged_users', fallback='accounts/login.html', message="You need to be logged in to create an article")
    def post(self, request):
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        image = request.FILES.get('article_image', False)
        image_url = ''
        if (image):
            key = "%s_%s.jpg" % (request.user.username, datetime.now())
            image_url = uploader.upload(image, key)
        article = Article.objects.create(user=request.user, title=title, content=content, category=category, image_url=image_url)
        tags = request.POST.get('tags', '').strip().split(",")
        if len(tags) > 0:
            for tag in tags:
                tag = tag.strip()
                if tag:
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
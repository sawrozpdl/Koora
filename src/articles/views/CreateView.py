from django.views import View
from django.template import loader
from django.http import HttpResponse
from articles.models import Article
from articles.models import Tag
from django.conf import settings
from utils import uploader

class CreateView(View):

    def get(self, request):
        return HttpResponse(loader.get_template('articles/create_article.html').render({
            "guide" : "Fill up your article and Click Post to publish and Draft to save it as a Draft",
            "categories" : settings.KOORA_CATEGORIES
        }, request))

    def post(self, request):
        title = request.POST['title']
        content = request.POST['content']
        tags = request.POST['tags'].split(", ")
        category = request.POST['category']
        image = request.FILES['article_image']
        image_url = ''
        if (image):
            key = "%s_%s.jpg" % (request.user.username, title)
            image_url = uploader.upload(image, key)
        article = Article.objects.create(title=title, content=content, category=category, image_url=image_url)
        if tags:
            for tag in tags:
                existing_tag = Tag.objects.filter(name=tag)
                if existing_tag.exists():
                    article.tags.add(existing_tag)
                else:
                    new_tag = Tag.objects.create(name=tag, description='nonefornow')
                    article.tags.add(new_tag)
            article.save()
        return HttpResponse(loader.get_template("articles/create_article.html").render({
            "success" : "Article creation successful!"
        }, request))
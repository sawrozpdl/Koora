from django.views import View
from django.template import loader
from django.http import HttpResponse
from articles.models import Article
from django.conf import settings
from utils import uploader

class UpdateView(View):

    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        return HttpResponse(loader.get_template('articles/update_article.html').render({
            "page_name": "articles",
            "messages" : [
                {
                    "type" : "warning",
                    "content" : "Change required field and Press Update to Publish the new verson of your Article"
                }
            ],
            "categories" : settings.KOORA_CATEGORIES,
            "article" : article,
            "tags" : article.get_tag_string()
        }, request))

    def post(self, request, slug):
        article = Article.objects.get(slug=slug)
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.category = request.POST['category']
        image = request.FILES.get('article_image', False)
        image_url = ''
        if (image):
            key = "%s_%s.jpg" % (request.user.username, article.title)
            image_url = uploader.upload(image, key)
            article.image_url = image_url
        article.remove_tags()
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
            "messages" : [
                {
                    "type" : "success",
                    "content" : "Article Updated!"
                }
            ],
            "page_name": "create_article"
        }, request))
        
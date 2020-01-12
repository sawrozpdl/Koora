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
            "guide" : "Change required field and Press Update to Publish the new verson of your Article",
            "categories" : settings.KOORA_CATEGORIES,
            "article" : article
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
        tags = request.POST.get('tags', '').split(", ")
        # if tags:
        #     for tag in tags:
        #         existing_tag = Tag.objects.filter(name=tag)
        #         if existing_tag.exists():
        #             article.tags.add(existing_tag)
        #         else:
        #             new_tag = Tag.objects.create(name=tag, description='nonefornow')
        #             article.tags.add(new_tag)
        article.save()
        return HttpResponse(loader.get_template("articles/create_article.html").render({
            "success" : "Article Updated!"
        }, request))
        
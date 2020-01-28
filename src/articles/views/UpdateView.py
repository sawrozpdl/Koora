from django.views import View
from django.urls import reverse
from django.conf import settings
from django.template import loader
from articles.models import Article
from utils.decorators import fail_safe, protected_view
from django.http import HttpResponse, HttpResponseRedirect
from utils.koora import setTagsFor, uploadImageFor, deleteImageFor
class UpdateView(View):

    @fail_safe(for_model=Article)
    def get(self, request, slug):

        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        article = Article.objects.get(slug=slug)

        return HttpResponse(loader.get_template('articles/post_article.html').render({
            "page_name": "articles",
            "messages" : [
                {
                    "type" : "warning",
                    "content" : "Change required field and Press Update to Publish the new verson of your Article"
                }
            ],
            "article" : article,
            "update_mode" : True,
            "tags" : article.get_tag_string()
        }, request))



    @fail_safe(for_model=Article)
    @protected_view(allow='logged_users', fallback='accounts/login.html', message="You don't have access to the page")
    def post(self, request, slug):

        article = Article.objects.get(slug=slug)

        article.title = request.POST['title']
        article.content = request.POST['content']
        article.category = request.POST['category']
        image = request.FILES.get('article_image', False)
        
        post_type=request.POST.get('post_type', 'public')
        article.is_private = post_type == 'private'

        if image:
            deleteImageFor(article)
            uploadImageFor(article, image, request.user.username)

        article.remove_tags()

        tags = request.POST.get('tags', '').strip().split(",")
        
        setTagsFor(article, tags)

        article.save()

        return HttpResponseRedirect(article.absolute_url)
    
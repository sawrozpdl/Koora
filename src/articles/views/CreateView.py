from django.views import View
from django.conf import settings
from django.template import loader
from articles.models import Article
from utils.decorators import protected_view, fail_safe
from django.http import HttpResponse, HttpResponseRedirect
from utils.koora import setTagsFor, uploadImageFor, get_message_or_default, generate_url_for

class CreateView(View):

    def get(self, request):

        message = get_message_or_default(request, {
            "type" : "warning",
            "content" : "Fill up your article and Click Post to publish and Draft to save it as a Draft"
        })

        return HttpResponse(loader.get_template('articles/post_article.html').render({
            "page_name" : "create_article",
            "message" : message
        }, request))


    @fail_safe(for_model=Article)
    @protected_view(allow='logged_users', fallback='accounts/login.html', message="You need to be logged in to create an article")
    def post(self, request):

        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        image = request.FILES.get('article_image', False)

        post_type=request.POST.get('post_type', 'public')
        post_mode=request.POST.get('post_mode', 'publish')

        is_private = post_type == 'private'
        is_drafted = post_mode == 'draft'

        article = Article.objects.create(user=request.user, title=title, content=content, category=category, is_drafted = is_drafted, is_private=is_private)

        if (image):
            uploadImageFor(article, image, request.user.username)
            
        tags = request.POST.get('tags', '').strip().split(",")
        
        setTagsFor(article, tags)
            
        article.save()
        
        if not is_drafted:
            return HttpResponseRedirect(article.absolute_url)
        else:
            return HttpResponseRedirect(generate_url_for('articles:create', query = {
                "type" : "success",
                "content" : "Article Drafted, to publish it, go to your profile"
            }))
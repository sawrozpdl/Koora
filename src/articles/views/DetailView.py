from django.views import View
from django.template import loader
from articles.models import Article
from comments.models import Comment
from utils.koora import deleteImageFor, get_message_or_default, generate_url_for
from utils.decorators import fail_safe, protected_view
from django.http import HttpResponse, HttpResponseRedirect

class DetailView(View):

    #@fail_safe(for_model=Article)
    def get(self, request, slug):

        article = Article.objects.get(slug=slug)

        message = get_message_or_default(request, {})

        template = loader.get_template("articles/article.html")
        content = {
            "page_name": "articles",
            "article": article,
            "message" : message,
            "vote_type" : article.get_user_vote(request.user),
            "comments" : article.comments
        }
        return HttpResponse(template.render(content, request))


    @fail_safe(for_model=Article)
    @protected_view(allow='logged_users', fallback='accounts/login.html', message="Login to post/delete contents")
    def post(self, request, slug):

        article = Article.objects.get(slug=slug)
        deleteMode = request.POST.get('deletemode', False)

        if deleteMode:
            
            if article.image_url:
                deleteImageFor(article)
            article.delete()

            return HttpResponseRedirect(generate_url_for("articles:list", query={
                "type" : "success",
                "content" : "Article deletion successful!"
            }))

        else:
            user = request.user

            content = request.POST.get('content', '')
            object_id = request.POST.get('object_id', 1)
            content_type=article.content_type

            Comment.objects.create(user=user, content=content,object_id=object_id,content_type=content_type)

            return HttpResponseRedirect(generate_url_for("articles:detail", kwargs={
                "slug" : slug
            }, query={
                "type" : "success",
                "content" : "Comment Added!"
            }))

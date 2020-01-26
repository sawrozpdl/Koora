from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from articles.models import Article
from comments.models import Comment
from utils.decorators import fail_safe, protected_view

class DetailView(View):

    @fail_safe(for_model=Article)
    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        template = loader.get_template("articles/article.html")
        content = {
            "page_name": "articles",
            "article": article,
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
        else:
            user = request.user
            content = request.POST.get('content', '')
            object_id = request.POST.get('object_id', 1)
            content_type=article.content_type
            Comment.objects.create(user=user, content=content,object_id=object_id,content_type=content_type)
            template = loader.get_template("articles/article.html")
            content = {
                "page_name": "articles",
                "article": article,
                "messages" : [
                    {
                        "type" : "success",
                        "content" : "Comment Added!"
                    }
                ],
                "comments" : article.comments
            }
            return HttpResponse(template.render(content, request))

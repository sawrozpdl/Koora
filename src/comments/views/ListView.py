from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from articles.models import Article
from comments.models import Comment

class ListView(View):

    def get(self, request, article_slug, comment_slug):
        pass

    def post(self, request, article_slug, comment_slug):
        pass
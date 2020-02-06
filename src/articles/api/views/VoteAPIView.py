import json
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
from utils.decorators import fail_safe_api
from django.contrib.auth.models import User
from utils.request import parse_body, set_user
from articles.models import Article, Tag, Vote
from django.contrib.contenttypes.models import ContentType

class VoteAPIView(View):

    def dispatch(self, request, *args, **kwargs):
        set_user(request)
        if request.user.is_authenticated:
            parse_body(request, for_method=request.method)
        return super(VoteAPIView, self).dispatch(request, *args, **kwargs)


    def get(self, request):
        return Http404()


    @fail_safe_api(for_model=User)
    def post(self, request):
        data = json.loads(request.body)
        article_id = data['article_id']
        vote_type = data['vote_type']

        try:
            content_type = ContentType.objects.get_for_model(Article)
            article = Article.objects.get(id=article_id)
            user = request.user
        except:
            return JsonResponse({
                'status' : 500
            })
        
        try:
            vote = Vote.objects.of_instance(article).get(user=user)
        except Vote.DoesNotExist:
            vote = False

        if vote:
            if (vote.is_upvote and vote_type == 'up') or (not vote.is_upvote and vote_type == 'down'):
                vote.delete()
            elif vote.is_upvote:
                vote.is_upvote = False
                vote.save()
            else:
                vote.is_upvote = True
                vote.save()
        else:
            is_upvote = True if vote_type == 'up' else False
            vote = Vote.objects.create(object_id=article_id, user=user, content_type=content_type, is_upvote=is_upvote)
            vote.save()

        data = {
            'status' : 200,
            'vote_count' : article.vote_count
        }
        return JsonResponse(data)
    
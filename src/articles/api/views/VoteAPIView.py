import json
from django.views import View
from django.http import Http404
from django.http import JsonResponse
from utils.decorators import fail_safe_api
from django.contrib.auth.models import User
from utils.request import parse_body, set_user
from articles.models import Article, Comment, Tag, Vote
from django.contrib.contenttypes.models import ContentType

class VoteAPIView(View):

    def dispatch(self, request, *args, **kwargs):
        set_user(request)
        if request.user.is_authenticated:
            parse_body(request, for_method=request.method)
        return super(VoteAPIView, self).dispatch(request, *args, **kwargs)


    def get(self, request):
        return Http404()


    @fail_safe_api(for_model=User, needs_authentication=True)
    def post(self, request):
        data = json.loads(request.body)
        object_id = data['object_id']
        model_name = data['model_name']
        vote_type = data['vote_type']

        content_type = ContentType.objects.get(model=model_name)
        model_class = content_type.model_class()

        user = request.user

        voted_object = model_class.objects.get(id=object_id)
        
        try:
            vote = Vote.objects.of_instance(voted_object).get(user=user)
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
            vote = Vote.objects.create(object_id=object_id, user=user, content_type=content_type, is_upvote=is_upvote)
            vote.save()

        data = {
            'status' : 200,
            'vote_count' : voted_object.vote_count
        }
        return JsonResponse(data)
    
from django.views import View
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError
from ..models import Questions
from comments.models import Comment

class DetailView(View):

    def get(self, request, slug):
        # try:
        Question = Question.objects.get(slug=slug)
        template = loader.get_template("questions/Question.html")
        print('this is vote: ', Question.get_user_vote(request.user))
        content = {
            "page_name": "Questions",
            "Question": Question,
            "vote_type" : Question.get_user_vote(request.user),
            "comments" : Question.comments
        }
        return HttpResponse(template.render(content, request))
        # except Question.DoesNotExist:
        #     raise Http404()
        # except:
        #     return HttpResponseServerError()

    def post(self, request, slug):
        # try:
        Question = Question.objects.get(slug=slug)
        deleteMode = request.POST.get('deletemode', False)
        if deleteMode:
            Question.delete()
            Questions = Question.objects.all()
            template = loader.get_template("Questions/Questions.html")
            content = {
                "page_name": "Questions",
                "messages" : [
                    {
                        "type" : "success",
                        "content" : "Question deletion successful!"
                    }
                ],
                "title" : "Questions by Users:",
                "Questions" : Questions
            }
            return HttpResponse(template.render(content, request))
        else:
            user = request.user
            content = request.POST.get('content', '')
            object_id = request.POST.get('object_id', 1)
            content_type=Question.content_type
            Comment.objects.create(user=user, content=content,object_id=object_id,content_type=content_type)
            template = loader.get_template("Questions/Question.html")
            content = {
                "page_name": "Questions",
                "Question": Question,
                "messages" : [
                    {
                        "type" : "success",
                        "content" : "Comment Added!"
                    }
                ],
                "comments" : Question.comments
            }
            return HttpResponse(template.render(content, request))
        # except Question.DoesNotExist:
        #     raise Http404()
        # except:
        #     return HttpResponseServerError()
        

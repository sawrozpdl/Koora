from django.views import View 
from questions.models import Questions
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError

class CreateView(View):

    def get(self, request):
        return HttpResponse(loader.get_template('questions/create_question.html').render({
            "page_name" : "ask_question",
            "message" : {
                "type" : "warning",
                "content" : "You may create your question here!"
            },
        }, request))

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden() # redirect to login 
        try:
       
            question = request.POST.get('Create_Question', 'ques')
            elaborate = request.POST.get('Elaborate_Question', 'elb')
            question = Questions.objects.create(user=request.user, category=category,Create_Question=question,Elaborate_Question=elaborate)
            question.save()
            return HttpResponse(loader.get_template("questions/create_question.html").render({
                "page_name" : "create_question",
                "messages" : [
                    {
                        "type" : "success",
                        "content" : "Your question has been added!"
                    }
                ]
            }, request))
        except:
            return HttpResponseServerError()






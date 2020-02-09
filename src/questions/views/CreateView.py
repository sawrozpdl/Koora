from django.views import View 
from questions.models import Questions
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseServerError

class CreateView(View):

    def get(self, request):
        return HttpResponse(loader.get_template('questions/create_question.html').render({
            "page_name" : "ask_question",
            "messages" : [
                {
                    "type" : "warning",
                    "content" : "You may create your question here!"
                }
            ],
        }, request))

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden() # redirect to login 
        try:
       
            category = request.POST['category']
            question = request.POST['question']
            elaborate = request.POST['elaborate']
            question = question.objects.create(category=category,question=question,elaborate=elaborate)
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




           
def Question1(request):
    return render(request,'questions/create_question.html')

def Question_save(request):
    if request.method== 'POST': 
        Create_Question =request.POST['Create_Question']
        Elaborate_Question= request.POST['Elaborate_Question']
        
        Question_obj = Questions(Create_Question=get_Create_Question,Elaborate_Question=get_Elaborate_Question)
        Question_obj.save()
        return HttpResponse("Save record!!")
    else:
        return HttpResponse("Error record saving!!")





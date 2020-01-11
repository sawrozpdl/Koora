from django.views import View
from django.template import loader
from django.http import HttpResponse

class UpdateView(View):

    def get(self, request, article_id):
        return HttpResponse('Update is under construction!')

    def post(self, request, article_id):
        pass
from django.http import HttpResponse
import os

def hello(request):
    return HttpResponse("Jibesh Gandu")

def read_file(request,filename):
   f = open(filename,'r')
   file_content = f.read()
   f.close()
   return HttpResponse(file_content, content_type="text/plain")
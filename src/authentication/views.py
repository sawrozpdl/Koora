from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode

def authorize(request):
  pass


def refresh(request):
  pass


def logout(request):
  togo = request.GET.get('next', reverse('accounts:login'))
  response = HttpResponseRedirect(togo + '?' + urlencode(request.GET.dict()))
  response.delete_cookie('accessToken')
  return response




from django.shortcuts import render

def prof(request):
    return render(request,'../templates/profile/profile.html')

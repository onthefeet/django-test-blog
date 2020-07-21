from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.http import HttpResponse
from newapp import views
# Create your views here.
def register(response):
    if response.method == 'POST':
        username=response.POST['username']
        password=response.POST['password']
        User.objects.create_user(username=username,password=password)
        return views.home(response)
    # elif response.method == 'GET':
        # return views.home(response)
    return render(response,"register/index.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return views.create(request)
        else:
            return views.home(request)
    return render(request, 'register/login.html')
    
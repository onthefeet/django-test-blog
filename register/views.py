from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import IntegrityError
from newapp import views
# Create your views here.
def register(response):
    if response.method == 'POST':
        try:
            username=response.POST['username']
            password=response.POST['password']
            User.objects.create_user(username=username,password=password)
            return redirect('/login')
        except IntegrityError :
            print("hello")
        except ValueError:
            print("haha")
    return render(response,"register/index.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(1800)
            return redirect('/')
    return render(request, 'register/login.html')

def user_logout(request):
    logout(request)
    return redirect('/')
    
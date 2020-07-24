from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Post,createPost
from django.contrib.auth.models import User
from django.utils import timezone
from register import views
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(response):
    if response.user.is_authenticated:
        query=response.GET.get("q")
        if query:
            posts=Post.objects.filter(title__icontains=query).order_by('published_date')
            return render(response,"newapp/base.html",{'posts':posts})
        else:

            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
            return render(response,"newapp/base.html",{'posts':posts})
    else:
        return views.user_login(response) 

def test(response):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(response,"newapp/home.html",{'posts':posts})

@login_required
def create(response):
    admin=response.user
    if response.method == 'POST':
        create = createPost(response.POST)
        if create.is_valid():
            post=Post(author=admin,title=create.cleaned_data["title"],text=create.cleaned_data["text"])
            post.publish()
            return redirect('/')
    else:
        create = createPost()
    create=createPost()
    choice=Post.objects.all()
    return render(response,"newapp/create.html",{'form':create,'choice':choice})

def search(request):
    pass
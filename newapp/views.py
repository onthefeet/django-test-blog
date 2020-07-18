from django.shortcuts import render
from django.http import HttpResponse
from .models import Post,createPost
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.
def home(response):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(response,"newapp/base.html",{'posts':posts})
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # return render(request, 'blog/post_list.html', {'posts': posts})

def test(response):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(response,"newapp/home.html",{'posts':posts})


def create(response):
    if response.method == 'POST':
        create = createPost(response.POST)
        if create.is_valid():
            admin=User.objects.get(username="admin")
            post=Post(author=admin,title=create.cleaned_data["title"],text=create.cleaned_data["text"])
            post.publish()
            return home(response)
    else:
        create = createPost()
    create=createPost()
    return render(response,"newapp/create.html",{'form':create})

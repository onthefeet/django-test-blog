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
    admin=response.user
    if response.method == 'POST':
        create = createPost(response.POST)
        if create.is_valid():
            post=Post(author=admin,title=create.cleaned_data["title"],text=create.cleaned_data["text"])
            post.publish()
            return home(response)
            # print(response.POST['choice'])
    else:
        create = createPost()
    create=createPost()
    choice=Post.objects.all()
    return render(response,"newapp/create.html",{'form':create,'choice':choice})

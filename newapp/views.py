from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.
def home(response):
    post=Post.objects.first()
    return render(response,"newapp/base.html")
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # return render(request, 'blog/post_list.html', {'posts': posts})

def test(response):
    return render(response,"newapp/home.html")

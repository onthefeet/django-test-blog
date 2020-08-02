from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Post,createPost
from django.contrib.auth.models import User
from django.utils import timezone
from register import views
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import forms
from .models import createPost
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag


# Create your views here.
def home(response):
    current=response.user
    most_common = Post.tags.most_common()[:10]
    if response.user.is_authenticated:
        query=response.GET.get("q")
        if query:
            user=User.objects.all()
            posts=Post.objects.filter(Q(title__icontains=query)|
            Q(text__icontains=query)|Q(author__username__icontains=query)).order_by('-published_date')
            return render(response,"newapp/home.html",{'posts':posts})
        else:
            post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
            p = Paginator(post_list,5)
            page_number=response.GET.get('page')
            try:
                posts=p.page(page_number)
            except PageNotAnInteger:
                posts=p.page(1)
            except EmptyPage:
                posts=p.page(p.num_pages)

            page_obj=p.get_page(page_number)
            context= {
                'posts':posts,'curr':current,'page_obj':page_obj,
                'common':most_common
            }
            return render(response,"newapp/home.html",context)
    else:
        return views.user_login(response) 

def test(response,pk):
    post = get_object_or_404(Post, pk=pk)
    if response.method =='GET':
        return render(response,"newapp/article.html",{'post':post})

@login_required
def create(response):
    admin=response.user
    if response.method == 'POST':
        create = createPost(response.POST)
        if create.is_valid():
            post=Post(author=admin,title=create.cleaned_data["title"],text=create.cleaned_data["text"],description=create.cleaned_data["description"])
            post.save()
            post.tags.add(*create.cleaned_data["tags"])
            post.publish()
            return redirect('/')
    else:
        create = createPost()
    return render(response,"newapp/create.html",{'form':create,'custom':"Create"})


def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form =createPost(request.POST,instance=post)
        if form.is_valid():
            post.author = request.user
            post.tags.set(*form.cleaned_data["tags"],clear=False)
            post.publish()
            return redirect('home')
    else:
        form = createPost(instance=post)
    return render(request, 'newapp/create.html', {'form': form,'custom':"Edit"})

def delete(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form=createPost(request.POST,instance=post)
        form.set_disable(instance=post)
        post.delete()
        return redirect('home')
    else:
        form = createPost(instance=post)
        form.set_disable(instance=post)
    return render(request,'newapp/create.html',{'form':form,'custom':"Delete"})

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'posts':posts,
    }
    return render(request, 'newapp/home.html', context)

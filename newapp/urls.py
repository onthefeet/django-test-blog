from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('create/',views.create,name='create'),
    re_path(r'^post/(?P<pk>[0-9]+)/edit/$', views.edit, name='edit'),
    re_path(r'^post/(?P<pk>[0-9]+)/delete/$', views.delete, name='delete'),
    re_path(r'^post/(?P<pk>[0-9]+)/test/$', views.test, name='article'),
]
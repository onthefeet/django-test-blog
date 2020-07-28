from django.urls import path,re_path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('test/',views.test, name='test'),
    path('create/',views.create,name='create'),
    re_path(r'^post/(?P<pk>[0-9]+)/edit/$', views.edit, name='edit'),
    re_path(r'^post/(?P<pk>[0-9]+)/delete/$', views.delete, name='delete'),
]
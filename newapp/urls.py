from django.urls import path
from . import views

url = [
    path('',views.home,name = 'home')
]
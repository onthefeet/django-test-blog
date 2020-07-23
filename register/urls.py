from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/',views.user_login, name="login"),
    path('create/login/',views.user_login, name="login"),
    path('register/logout/',views.user_logout,name="user_logout")
]
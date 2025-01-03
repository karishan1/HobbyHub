"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from .views import login_view,home_view,logout_view,signup_view,user_view,user_list_view,current_user_view



from .views import main_spa

urlpatterns = [
    path("main/", main_spa),
    path("", login_view, name="login"),
    path("home/", home_view, name="home"),
    path("logout/",logout_view, name = "logout"),
    path("signup/",signup_view, name = "signup"),
    path("user/",user_view,name="user"),
    path("user_list/",user_list_view,name="user_list"),
    path("api/current-user/",current_user_view, name = "current_user"),

    
]

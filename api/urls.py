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
from . import views


from .views import main_spa

urlpatterns = [
    path("main/", main_spa),
    path("", views.login_view, name="login"),
    path("home/", views.home_view, name="home"),
    path("logout/",views.logout_view, name = "logout"),
    path("signup/",views.signup_view, name = "signup"),
    path("user_list/",views.user_list_view,name="user_list"),
    path("current-user/",views.current_user_view, name = "current_user"),
    path("hobby_db/", views.hobby_db_view, name="add_hobby_to_db"),
    path("friend_request/", views.friend_request_view , name="send_friend_request"),
    path("friendships/", views.friendship_view , name="friendships"),
    path("get_csrf_token/", views.get_csrf_token, name="get_csrf_token"),
    
]

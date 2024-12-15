from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, redirect
from .models import Hobby
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



import json


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


def view_hobby(request):
    if request.method == 'GET':
        all_hobbies = Hobby.objects.all()
        hobby_list = [x.__str__() for x in all_hobbies]
        return JsonResponse(hobby_list,safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        new_hobby = Hobby.object.create(
            hobby_name = data['hobby_name']
        )
        return JsonResponse(new_hobby.__str___(),status=201)


def login_view(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home") 
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    
    return render(request, "login.html")  # Renders the login.html template for GET requests

def home_view(request):
    #hobbies = request.user.hobbies.all()
    return render(request, "home.html", {"user": request.user})


def logout_view(request):
    logout(request)
    return render(request, "login.html")
    # Redirect to a success page.

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")

        if password != confirm_password:
                return render(request, "signup.html", {"error": "Passwords do not match."})
        
        if not username or not password or not email:
            return render(request, "signup.html", {"error": "All fields are required."})
        
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already taken."})
        

        try:
            validate_password(password, user=User(username=username))
        except ValidationError as e:
            return render(request, "signup.html", {"error": e.messages[0]})
        
        hashed_password = make_password(password)
        
        user = User.objects.create(
            username=username,
            email=email,
            password=hashed_password 
        )
        user.save()

        login(request, user)
        return redirect("login")
    
    return render(request, "signup.html")

def user_view(request):
    if request.method == 'GET':
        User = get_user_model()
        all_users = User.objects.all()
        user_list = [x.to_dict() for x in all_users]
        return JsonResponse(user_list, safe=False)
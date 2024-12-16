from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, redirect
from .models import Hobby
from .forms import CustomUserCreationForm

from django.contrib.auth.forms import AuthenticationForm

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
    """
    Handle user login.
    """
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("http://localhost:5173/")  # Redirect to Vue frontend
        else:
            return render(request, "login.html", {"form": form, "error": "Invalid username or password."})
    
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})  # Render the login page fo

def home_view(request):
    #hobbies = request.user.hobbies.all()
    return render(request, "home.html", {"user": request.user})


def logout_view(request):
    logout(request)
    return render(request, "login.html")
    # Redirect to a success page.

def signup_view(request):
    """
    Handle user signup and account creation.
    """
    if request.method == "POST":
        print("Received POST request with data:", request.POST)  # Log incoming POST data
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log in the user
            return redirect("http://localhost:5173/")
        else:
            return render(request, "signup.html", {"form": form})  # Re-render with errors

    print("Rendering signup form for GET request.")  # Log GET request
    form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

def user_view(request):
    if request.method == 'GET':
        User = get_user_model()
        all_users = User.objects.all()
        user_list = [x.to_dict() for x in all_users]
        return JsonResponse(user_list, safe=False)
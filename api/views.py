from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Hobby

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
            return redirect("home")  # Replace 'profile' with your desired redirect URL name
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    
    return render(request, "login.html")  # Renders the login.html template for GET requests

def home_view(request):
    #hobbies = request.user.hobbies.all()
    return render(request, "home.html", {"user": request.user})


def logout_view(request):
    return render(request, "login.html")
    # Redirect to a success page.

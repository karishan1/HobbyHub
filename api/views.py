from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, redirect
from .models import Hobby
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

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
    return render(request, "login.html", {"form": form})

def home_view(request):
    #hobbies = request.user.hobbies.all()
    return render(request, "home.html", {"user": request.user})


def logout_view(request):
    logout(request)
    return render(request, "login.html")

def signup_view(request):
    """
    Handle user signup and account creation.
    """
    if request.method == "POST":
        print("Received POST request with data:", request.POST)  
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log in the user
            return redirect("http://localhost:5173/")
        else:
            return render(request, "signup.html", {"form": form})  

    print("Rendering signup form for GET request.") 
    form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

def user_view(request):
    if request.method == 'GET':
        User = get_user_model()
        all_users = User.objects.all()
        user_list = [x.to_dict() for x in all_users]
        return JsonResponse(user_list, safe=False)
    
def user_list_view(request):
    if request.method == 'GET':
        User = get_user_model()
        logged_user = request.user
        print(logged_user.id)
        all_users = User.objects.exclude(id=logged_user.id)

        min_age = request.GET.get('min_age',None)
        max_age = request.GET.get('max_age',None)

        if min_age:
            all_users = all_users.filter(DOB__lte=timezone.now() - timedelta(days=int(min_age)*365))
        if max_age:
            all_users = all_users.filter(DOB__gte=timezone.now() - timedelta(days=int(max_age)*365))

        page_number = request.GET.get('page', 1)
        paginator = Paginator(all_users, 10)
        page_object = paginator.get_page(page_number)

        user_list = [x.to_dict_user_list() for x in page_object]
        return JsonResponse(user_list, safe=False)


@login_required
def current_user_view(request):
    if request.user.is_authenticated:
        if request.method == "PUT":
            try:
                data = json.loads(request.body)
                
                user = request.user
                if "username" in data:
                    user.username = data["username"]
                if "email" in data:
                    user.email = data["email"]
                if "DOB" in data:
                    user.DOB = data["DOB"]  
                if "hobbies" in data:
                    if hasattr(user, "set_hobbies"):  
                        user.set_hobbies(data["hobbies"])
                
                user.save()
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "DOB": getattr(user, "DOB", None),
                    "hobbies": getattr(user, "get_hobbies", lambda: [])(),
                }
                return JsonResponse(user_data)
            
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        user_data = {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "DOB": getattr(request.user, "DOB", None),
            "hobbies": getattr(request.user, "get_hobbies", lambda: [])(),
        }
        return JsonResponse(user_data)

    else:
        return JsonResponse({"error": "User is not authenticated"}, status=401)
    
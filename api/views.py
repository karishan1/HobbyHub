from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, redirect
from .models import Hobby, User, FriendRequest, Friendship
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm
import json
from django.middleware.csrf import get_token
from django.db import IntegrityError


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


@login_required
def add_user_hobby(request):
    try:
        data = json.loads(request.body)
        user = request.user
        
        if not user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)
            
        hobby_id = data.get('hobby_id')
        if not hobby_id:
            return JsonResponse({"error": "Hobby ID is required"}, status=400)
            
        try:
            hobby = Hobby.objects.get(id=hobby_id)
        except Hobby.DoesNotExist:
            return JsonResponse({"error": "Hobby not found"}, status=404)

        user.Hobbies.add(hobby)
        return JsonResponse({
            "message": "Hobby added successfully",
            "hobby": {"id": hobby.id, "hobby_name": hobby.hobby_name}
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def add_hobby_to_db(request):
    """
    Adds a new hobby to the hobbies database.
    """
    try:
        data = json.loads(request.body)
        hobby_name = data.get('hobby_name')

        if not hobby_name:
            return JsonResponse({"error": "Hobby name is required"}, status=400)

        # Check if the hobby already exists, create it if not
        hobby, created = Hobby.objects.get_or_create(hobby_name=hobby_name)

        if not created:
            return JsonResponse({"message": "Hobby already exists."}, status=200)

        return JsonResponse({
            "message": "Hobby added to the database successfully.",
            "hobby": {"id": hobby.id, "hobby_name": hobby.hobby_name},
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def displayhobbies(request):
    if request.method == 'GET':
        # Fetch all hobbies from the database
        all_hobbies = Hobby.objects.all()
        hobby_list = [{'id': hobby.id, 'hobby_name': hobby.hobby_name} for hobby in all_hobbies]
        return JsonResponse(hobby_list, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    


@login_required
def remove_user_hobby(request):
    """
    Removes a hobby from the user's hobbies list.
    """
    try:
        data = json.loads(request.body)
        user = request.user

        hobby_name = data.get('hobby_name')
        if not hobby_name:
            return JsonResponse({"error": "Hobby name is required"}, status=400)

        # Fetch the hobby object by its name
        try:
            hobby = Hobby.objects.get(hobby_name=hobby_name)
        except Hobby.DoesNotExist:
            return JsonResponse({"error": "Hobby not found"}, status=404)

        # Remove the hobby from the user's Hobbies relationship
        user.Hobbies.remove(hobby)

        return JsonResponse({
            "message": "Hobby removed successfully.",
            "hobby_name": hobby_name,
        }, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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

@login_required
def user_view(request):
    if request.method == 'GET': 
        User = get_user_model()
        all_users = User.objects.all()
        user_list = [x.to_dict() for x in all_users]
        return JsonResponse(user_list, safe=False)
    
@login_required 
def user_list_view(request):
    if request.method == 'GET':
        User = get_user_model()

        logged_user = request.user
        all_users = User.objects.exclude(id = logged_user.id)

        min_age = request.GET.get('min_age',None)
        max_age = request.GET.get('max_age',None)

        today = now().date()

        if min_age:
            min_age_date = today - timedelta(days=int(min_age)*365)
            all_users = [x for x in all_users if x.DOB is not None and x.DOB <= min_age_date]
        if max_age:
            max_age_date = today - timedelta(days=int(max_age)*365)
            all_users = [x for x in all_users if x.DOB is not None and x.DOB >= max_age_date]

        logged_user_hobbies = set(logged_user.Hobbies.all())

        def get_common_hobby_count(user):
            user_hobbies = set(user.Hobbies.all())
            return len(logged_user_hobbies & user_hobbies)
        
        for i in range(len(all_users)):
            for j in range(i+1, len(all_users)):
                if get_common_hobby_count(all_users[j]) > get_common_hobby_count(all_users[i]):
                    temp = all_users[i]
                    all_users[i] = all_users[j]
                    all_users[j] = temp

        page_number = request.GET.get('page', 1)
        paginator = Paginator(all_users, 10)
        page_object = paginator.get_page(page_number)

        user_list = [x.to_dict_user_list() for x in page_object]

        response_data = {
            'user_list': user_list,
            'total_pages': paginator.num_pages,
            'current_page': page_object.number,
            'has_next': page_object.has_next(),
            'has_previous': page_object.has_previous(),
        }
        return JsonResponse(response_data, safe=False)
    

@login_required
def current_user_view(request):
    if request.method == "PUT": 
        try:
            data = json.loads(request.body)

            
            user = request.user
            user.username = data.get("username", user.username)
            user.email = data.get("email", user.email)
            user.DOB = data.get("DOB", user.DOB)
            if hasattr(user, "set_hobbies"):
                user.set_hobbies(data.get("hobbies", []))
            
            user.save()
            return JsonResponse({"message": "User updated successfully"})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    user_data = {
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
        "DOB": getattr(request.user, "DOB", None),
        "hobbies": getattr(request.user, "get_hobbies", lambda: [])(),
    }
    return JsonResponse(user_data)

@login_required
def friend_request_view(request):
            
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            from_user = request.user
            to_user_id = data.get("to_friend_id")
            to_user = User.objects.get(id = to_user_id)

            if FriendRequest.objects.filter(from_user = from_user, to_user = to_user).exists():
                return JsonResponse({"message" : "Already Sent"}, status = 400)
            elif FriendRequest.objects.filter(from_user = to_user, to_user = from_user).exists():
                return JsonResponse({"message" : "This person has already sent a friend request to you"}, status = 400)

            FriendRequest.objects.create(from_user = from_user, to_user=to_user)
            return JsonResponse({"message" : "Friend Request Sent"})
            
        except User.DoesNotExist:
            return JsonResponse({"message" : " User Does Not Exists"}, status = 404)
        
        except Exception as e:
            return JsonResponse({"message" : str(e)}, status = 500)
    
    elif request.method == "GET":
        to_user = request.user

        friend_request_list = FriendRequest.objects.filter(to_user = to_user)

        friend_request_list = [x.to_dict() for x in friend_request_list]

        return JsonResponse(friend_request_list, safe=False)
    
    elif request.method == "PUT":
        try:
            to_user = request.user
            data = json.loads(request.body)
            request_id = data.get("request_id")

            friend_request = FriendRequest.objects.filter(id = request_id, to_user = to_user).first()

            friend_request.status = "accepted"
            friend_request.save()

            from_user = friend_request.from_user

            try:

                Friendship.objects.create(user=from_user, friend=to_user)
                Friendship.objects.create(user=to_user, friend=from_user)

            except IntegrityError:
                return JsonResponse({"message" : "Friendship already exists"})

            return JsonResponse({"message" : "Friend request accepted and frienship established"})


        except User.DoesNotExist:
            return JsonResponse({"message" : " User Does Not Exists"}, status = 404)


        
    return JsonResponse({"message" : " Invalid Request"}, status = 405)

@login_required
def friendship_view(request):
    if request.method == "GET":

        local_user = request.user

        friendship_list = Friendship.objects.filter(user = local_user)

        friendship_list = [x.get_friend() for x in friendship_list]

        return JsonResponse(friendship_list, safe=False)





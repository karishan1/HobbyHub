from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from django.shortcuts import render, redirect
from .models import Hobby, User, FriendRequest, Friendship
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
import json
from django.middleware.csrf import get_token
from django.db import IntegrityError
from django.urls import reverse
from typing import List, Dict, Set, Optional, Tuple, Type, Any
from django.db.models.query import QuerySet
from datetime import date


def get_csrf_token(request: HttpRequest) -> JsonResponse:
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html')

def landing_page_view(request):
    return render(request, "landing.html")

@login_required
def hobby_db_view(request: HttpRequest) -> JsonResponse:
    """
    Adds a new hobby to the hobbies database.
    """
    if request.method == 'GET':
        # Fetch all hobbies from the database
        all_hobbies: QuerySet[Hobby] = Hobby.objects.all()
        hobby_list: List[Dict[str, any]] = [{'id': hobby.id, 'hobby_name': hobby.hobby_name} for hobby in all_hobbies]

        return JsonResponse(hobby_list, safe=False)
    
    elif request.method == 'POST':
        try:
            data: Dict = json.loads(request.body)
            hobby_name: str = data.get('hobby_name')

            if not hobby_name:
                return JsonResponse({"error": "Hobby name is required"}, status=400)

            result: Tuple[Hobby,bool] = Hobby.objects.get_or_create(hobby_name=hobby_name)
            hobby, created = result

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
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user login.
    """
    if request.method == "POST":
        form: AuthenticationForm = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user: User = form.get_user()
            login(request, user)
            return redirect(reverse("home")) # Redirect to Vue frontend
        else:
            return render(request, "login.html", {"form": form, "error": "Invalid username or password."})

    form: AuthenticationForm = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def home_view(request: HttpRequest) -> HttpResponse:
    #hobbies = request.user.hobbies.all()
    return render(request, "api/spa/index.html", {"user": request.user})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return render(request, "login.html")

def signup_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user signup and account creation.
    """
    if request.method == "POST":
        print("Received POST request with data:", request.POST)  
        form: CustomUserCreationForm = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user: User = form.save()  # Save the new user
            login(request, user)  # Log in the user
            return redirect(reverse("home"))
        else:
            return render(request, "signup.html", {"form": form})  

    print("Rendering signup form for GET request.") 
    form: CustomUserCreationForm = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


    
@login_required 
def user_list_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        UserModel: Type[User] = get_user_model()

        logged_user: User = request.user
        all_users: QuerySet[User] = UserModel.objects.exclude(id = logged_user.id)

        min_age: Optional[int] = request.GET.get('min_age',None)
        max_age: Optional[int] = request.GET.get('max_age',None)

        today: date = now().date()

        if min_age:
            min_age_date: date = today - timedelta(days=int(min_age)*365)
            all_users = [x for x in all_users if x.DOB is not None and x.DOB <= min_age_date]
        if max_age:
            max_age_date: date = today - timedelta(days=int(max_age)*365)
            all_users = [x for x in all_users if x.DOB is not None and x.DOB >= max_age_date]

        logged_user_hobbies: Set[Hobby] = set(logged_user.Hobbies.all())

        def get_common_hobby_count(user: User) -> int:
            user_hobbies: Set[Hobby] = set(user.Hobbies.all())
            return len(logged_user_hobbies & user_hobbies)
        
        for i in range(len(all_users)):
            for j in range(i+1, len(all_users)):
                if get_common_hobby_count(all_users[j]) > get_common_hobby_count(all_users[i]):
                    temp: User = all_users[i]
                    all_users[i] = all_users[j]
                    all_users[j] = temp

        page_number: int = request.GET.get('page', 1)
        paginator: Paginator = Paginator(all_users, 10)
        page_object: Page = paginator.get_page(page_number)

        user_list: List[Dict[str, Any]] = [x.to_dict_user_list() for x in page_object]

        response_data: Dict[str, Any] = {
            'user_list': user_list,
            'total_pages': paginator.num_pages,
            'current_page': page_object.number,
            'has_next': page_object.has_next(),
            'has_previous': page_object.has_previous(),
        }
        return JsonResponse(response_data, safe=False)
    

@login_required
def current_user_view(request: HttpRequest) -> JsonResponse:
    if request.method == "PUT":
        try:

            data: Dict = json.loads(request.body)
            action: str = data.get('action')

            if not action:
                try:
                    form: CustomUserUpdateForm = CustomUserUpdateForm(data, instance=request.user)
                    if form.is_valid():
                        form.save()
                        return JsonResponse({"message": "User details updated successfully!"})
                    else:
                        print(form.errors)
                        return JsonResponse({"errors": form.errors}, status=400)
                    
                except json.JSONDecodeError:
                    return JsonResponse({"error": "Invalid JSON data."}, status=400)
            
            elif action == "add hobby":
                try:
                    user: User = request.user

                    if not user.is_authenticated:
                        return JsonResponse({"error": "User not authenticated"}, status=401)
                        
                    hobby_id: int = data.get('hobby_id')

                    if not hobby_id:
                        return JsonResponse({"error": "Hobby ID is required"}, status=400)
                        
                    try:
                        hobby: Hobby = Hobby.objects.get(id=hobby_id)

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
                
            elif action == "remove hobby":
                try:
                    user: User = request.user

                    hobby_name: str = data.get('hobby_name')

                    if not hobby_name:
                        return JsonResponse({"error": "Hobby name is required"}, status=400)

                    # Fetch the hobby object by its name
                    try:
                        hobby: Hobby = Hobby.objects.get(hobby_name=hobby_name)

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
            
            elif action == "change password":
                try:
                    form: PasswordChangeForm = PasswordChangeForm(user=request.user, data=data)
                    if form.is_valid():
                        user: User = form.save()
                        update_session_auth_hash(request, user)

                        return JsonResponse({"message": "Password changed successfully!"})
                    else:
                        print("Form Errors:", form.errors) 
                        return JsonResponse({"errors": form.errors}, status=400)
                    
                except json.JSONDecodeError:
                    return JsonResponse({"message": "Invalid JSON data."}, status=400)   
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
    elif request.method == "GET":
        # Return current user data
        user_data: Dict[str, Any] = {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "DOB": getattr(request.user, "DOB", None),
            "hobbies": getattr(request.user, "get_hobbies", lambda: [])(),
        }
        return JsonResponse(user_data)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@login_required
def friend_request_view(request: HttpRequest) -> JsonResponse:
            
    if request.method == "POST":
        try:
            data: Dict = json.loads(request.body)

            from_user: User = request.user
            to_user_id: int = data.get("to_friend_id")
            to_user: User = User.objects.get(id = to_user_id)

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
        to_user: User = request.user

        friend_request_list_query_set: QuerySet[FriendRequest] = FriendRequest.objects.filter(to_user = to_user)

        friend_request_list: List[Dict[str, Any]] = [x.to_dict() for x in friend_request_list_query_set]

        return JsonResponse(friend_request_list, safe=False)
    
    elif request.method == "PUT":
        try:
            to_user: User = request.user
            data: Dict = json.loads(request.body)
            request_id: int = data.get("request_id")

            friend_request: Optional[FriendRequest] = FriendRequest.objects.filter(id = request_id, to_user = to_user).first()

            friend_request.status = "accepted"
            friend_request.save()

            from_user: User = friend_request.from_user

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
def friendship_view(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":

        local_user: User = request.user

        friendship_list_query_set: QuerySet[Friendship] = Friendship.objects.filter(user = local_user)

        friendship_list: List[Dict[str, Any]] = [x.get_friend() for x in friendship_list_query_set]

        return JsonResponse(friendship_list, safe=False)

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
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




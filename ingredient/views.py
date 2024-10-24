from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
# from main.forms import MoodEntryForm
from fnb.views import show_fnb
from fnb.models import Fnb
from ingredient.models import Ingredient
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count
from django.template.loader import render_to_string

# Create your views here.

def show_filter(request):
    ingredient = Ingredient.objects.all()
    fnb = Fnb.objects.all()

    context = {"ingredients" : ingredient,"fnb" : fnb}

    return render(request,"show_filter.html",context)

@csrf_exempt  # To handle the AJAX POST request
def record_ingredients(request):
    if request.method == "POST":
        try:
            # Parse the JSON data
            data = json.loads(request.body)
            ingredients = data.get('ingredients', [])

            print("Selected ingredient:", ingredients)

            ingredient_objects = Ingredient.objects.filter(name__in=ingredients)


            fnb_set = set()

            for ingredient in ingredient_objects:
                food = set(ingredient.fnb.all())

                if len(fnb_set) == 0:
                    fnb_set = food
                else:
                    fnb_set.intersection_update(food)
                

            
            
            context = {'fnbs': fnb_set}
            
            html = render_to_string('fnb_kosong.html', context)
            
            return JsonResponse({'html': html})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"})

def show_card(request):
    return render(request,"nyoba2.html")

def show_fnb_json(request):
    data = Fnb.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
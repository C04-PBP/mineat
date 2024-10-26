from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.paginator import Paginator
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

    # Retrieve the page number from the query string
    page_number = request.GET.get("page", 1)

    # Set up pagination
    paginator = Paginator(fnb, 6)
    page_obj = paginator.get_page(page_number)

    # If AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('fnb_kosong.html', {"fnbs": page_obj})
        return JsonResponse({'html': html})
    
    # For non-AJAX, render the full page
    context = {"ingredients": ingredient, "fnb": page_obj}
    return render(request, "show_filter.html", context)

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

            if len(ingredients) == 0:
                fnb = Fnb.objects.all()
                paginator = Paginator(fnb,6)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)
                context = {'fnbs': page_obj}
            
            else:
                fnb = list(fnb_set)
                paginator = Paginator(fnb,6)
                page_number = request.GET.get("page")
                page_obj = paginator.get_page(page_number)
                context = {'fnbs': page_obj}
            
            html = render_to_string('fnb_kosong.html', context)
            
            return JsonResponse({'html': html})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    
    return JsonResponse({"status": "error", "message": "Invalid request"})

def search_ingredient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ingredient_query = data.get('ingredient', '')

        # Filter ingredients by partial match
        ingredients = Ingredient.objects.filter(name__icontains=ingredient_query)
        
        # Serialize the queryset to JSON
        serialized_ingredients = serializers.serialize('json', ingredients)
        
        return JsonResponse({'ingredients': serialized_ingredients})
    
def show_card(request):
    return render(request,"nyoba2.html")

def show_fnb_json(request):
    data = Fnb.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
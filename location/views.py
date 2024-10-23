from django.shortcuts import render
from location.models import Location
from restaurant.models import Restaurant
from restaurant.views import show_restaurant
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def show_location(request):
    location = Location.objects.all()

    context = {"locations" : location}

    return render(request,"show_location.html",context)

def get_restaurant(request):
    
    if request.method == "POST":
        try:
            # Parse the JSON data
            data = json.loads(request.body)
            location = data.get('location', [])

            location_object = Location.objects.filter(name=location)

            restaurants = Restaurant.objects.filter(location = location_object)
            
            for i in restaurants:
                print(i.name)

            return show_restaurant(request,restaurants)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"})
from django.shortcuts import render
from location.models import Location
from django.core import serializers
from restaurant.models import Restaurant
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.template.loader import render_to_string
from restaurant.views import show_json
from ingredient.models import Ingredient

# Create your views here.

def show_location(request):
    query = request.GET.get('q', '')
    if query:
        locations = Location.objects.filter(name__icontains=query)
    else:
        locations = Location.objects.all()

    context = {"locations": locations, "query": query}
    return render(request, "show_location.html", context)

def location_details(request):
    location_id = request.GET.get('id')
    location = Location.objects.get(id=location_id)
    restaurant = Restaurant.objects.filter(location=location)

    context = {
        "location": location,
        "restaurants": restaurant,
    }
    return render(request, "location_details.html", context)

def location_search_ajax(request):
    query = request.GET.get('q', '')
    if query:
        location = Location.objects.filter(name__icontains=query)
    else:
        location = Location.objects.all()

    html = render_to_string('hasil_search_location.html', {'locations': location})
    return JsonResponse({'html': html})

def update_trivia(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        location_id = data.get('id')
        new_trivia = data.get('trivia')

        try:
            location = Location.objects.get(id=location_id)
            location.trivia = new_trivia
            location.save()
            return JsonResponse({'success': True})
        except Location.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Location not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def show_json(request):
    data = []
    restaurant_data = []
    restaurantsInTheDistrict = []
    for i in Restaurant.objects.all():
        foods = []
        for j in i.fnb.all():
            

            ingredients_list = ""

            for ingredient in Ingredient.objects.filter(fnb=j):
                    ingredients_list += f"{ingredient.name}, "
            foods.append(
                {
                    "id" : j.id,
                    "title": j.name,
                    "price": j.price,
                    "description": j.description,
                    "ingredients": ingredients_list,
                    "imageUrl": j.image.url
                }
            )
        restaurant_data.append({
            "title": i.name,
            "address" : i.address,
            "district" : i.location.name,
            "imageUrl": i.image,
            "foodsInTheRestaurant": foods,
        })
    for k in Location.objects.all():
        for l in restaurant_data:
            if k.name == l['district']:
                print(k.name)
                print(l['district'])
                restaurantsInTheDistrict.append(l)
        data.append({
            "title": k.name,
            "imageUrl": k.image,
            "trivia": k.trivia,
            "restaurantsInTheDistrict": restaurantsInTheDistrict,
        })
        restaurantsInTheDistrict = []
    return JsonResponse(data,safe=False)


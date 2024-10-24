from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from restaurant.models import Restaurant
from location.models import Location

# Create your views here.

def show_restaurant(request):
    restaurants = Restaurant.objects.all()
    context = {
        "restaurants": restaurants
    }
    return render(request, "show_restaurant.html", context)

def ajax_search_restaurant(request):
    query = request.GET.get('q', '')
    if query:
        restaurants = Restaurant.objects.filter(name__icontains=query)
    else:
        restaurants = Restaurant.objects.all()

    html = render_to_string('hasil_search.html', {'restaurants': restaurants})
    return JsonResponse({'html': html})

def ajax_search_district(request):
    location_query = request.GET.get('location_q', '')

    if location_query:
        restaurants = Restaurant.objects.filter(location__name__icontains=location_query)
    else:
        restaurants = Restaurant.objects.all()

    html = render_to_string('hasil_search.html', {'restaurants': restaurants})
    return JsonResponse({'html': html})
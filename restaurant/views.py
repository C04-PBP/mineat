from django.shortcuts import render
from restaurant.models import Restaurant

# Create your views here.

def show_restaurant(request,restaurant = None):
    if restaurant:
        context = {
            "restaurants" : restaurant
        }
    else:
        context = {
            "restaurants" : Restaurant.objects.all()
        }

    return render(request,"show_restaurant.html",context)
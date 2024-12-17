from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from restaurant.models import Restaurant
from django.core import serializers
from location.models import Location
from restaurant.forms import RestaurantForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

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

    html = render_to_string('hasil_search_restaurant.html', {'restaurants': restaurants})
    return JsonResponse({'html': html})

def ajax_search_district(request):
    location_query = request.GET.get('location_q', '')

    if location_query:
        restaurants = Restaurant.objects.filter(location__name__icontains=location_query)
    else:
        restaurants = Restaurant.objects.all()

    html = render_to_string('hasil_search_restaurant.html', {'restaurants': restaurants})
    return JsonResponse({'html': html})

def ajax_search_fnb(request):
    fnb_query = request.GET.get('fnb_q', '')

    if fnb_query:
        restaurants = Restaurant.objects.filter(fnb__name__icontains=fnb_query).distinct()
    else:
        restaurants = Restaurant.objects.all()

    html = render_to_string('hasil_search_restaurant.html', {'restaurants': restaurants})
    return JsonResponse({'html': html})

def restaurant_details(request):
    restaurant_id = request.GET.get('id')
    restaurant = Restaurant.objects.get(id=restaurant_id)
    context = {
        "restaurant": restaurant,
        "fnb_items": restaurant.fnb.all(),
    }
    return render(request, "restaurant_details.html", context)

def add_restaurant(request):
    form = RestaurantForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        restaurant = form.save(commit=False)
        restaurant.save()
        form.save_m2m()
        return redirect('restaurant:show_restaurant')

    context = {'form': form}
    return render(request, "add_restaurant.html", context)

def delete_restaurant(request, id):
    restaurant = Restaurant.objects.get(pk=id)
    restaurant.delete()
    return HttpResponseRedirect(reverse('restaurant:show_restaurant'))

def edit_restaurant(request, id):
    order = Restaurant.objects.get(pk = id)

    form = RestaurantForm(request.POST or None, instance=order)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('restaurant:show_restaurant'))

    context = {'form': form}
    return render(request, "edit_restaurant.html", context)  

def add_restaurant_ajax(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            html = render_to_string('add_restaurant_ajax.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'html': html})
    else:
        form = RestaurantForm()
        html = render_to_string('add_restaurant_ajax.html', {'form': form}, request=request)
        return JsonResponse({'html': html})
    

def show_json(request):
    data = []
    for i in Restaurant.objects.all():
        data.append({
            "title": i.name,
            "address" : i.address,
            "district" : i.location.name,
            "imageUrl": i.image
        })
    return JsonResponse(data,safe=False)
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
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
from django.template.loader import render_to_string
from .forms import FnbForm

# Create your views here.
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('fnb:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('ingredient:show_filter')

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    return redirect('landing_page')

def show_fnb(request,food = None):
    if food:
        context = {
            "fnbs" : food
        }
    else:
        context = {
            "fnbs" : Fnb.objects.all()
        }
    return render(request,"show_fnb.html",context)

def add_fnb(request):
    if request.method == "POST":
        form = FnbForm(request.POST)
        if form.is_valid():
            fnb_instance = form.save(commit=False)  # Save the Fnb instance
            fnb_instance.user = request.user
            fnb_instance.save()

            # Link the Fnb instance to the selected ingredients
            selected_ingredients = form.cleaned_data['ingredients']
            for ingredient in selected_ingredients:
                ingredient.fnb.add(fnb_instance)  # Add the Fnb to each ingredient's fnb field

            return redirect('ingredient:show_filter')
        else:
            print("Form Errors:", form.errors)
    else:
        form = FnbForm()

    context = {'form': form}
    return render(request, "add_fnb.html", context)

def search_fnbs(request):
    query = request.GET.get('q', '')
    fnbs = Fnb.objects.filter(name__icontains=query) if query else Fnb.objects.all()
    
    # Render results to HTML
    html = render_to_string('fnb_kosong.html', {'fnbs': fnbs})
    return JsonResponse({'html': html})

def landing_page(request):
    return render(request, 'landing_page.html')

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Fnb

def add_fnb_ajax(request):
    if request.method == "POST":
        # Get form data from the request
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.POST.get("image")
        
        # Check if the user is authenticated
        if request.user.is_authenticated:
            try:
                # Create and save a new Fnb object
                new_fnb = Fnb(
                    name=name,
                    description=description,
                    price=price,
                    image=image,
                    user=request.user  # Set the user as the creator
                )
                new_fnb.save()

                # Optional: Send a JSON response with the new Fnb data
                return JsonResponse({"status": "created", "fnb": {
                    "name": name,
                    "description": description,
                    "price": price,
                    "image": image,
                }}, status=201)
            
            except Exception as e:
                # Log and return an error response
                print(f"Error saving Fnb: {e}")
                return JsonResponse({"status": "error", "message": str(e)}, status=500)
        else:
            # Return error if user is not authenticated
            return JsonResponse({"status": "error", "message": "User not authenticated"}, status=403)
    
    # Return an error if the request is not POST
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def show_json(request):
    data = []
    for i in Fnb.objects.all():
        ingredients_list = ""
        for ingredient in Ingredient.objects.filter(fnb=i):
            ingredients_list += f"{ingredient.name}, " 
        data.append({
            "title": i.name,
            "price": i.price,
            "description": i.description,
            "ingredients": ingredients_list,
            "imageUrl": i.image.url
        })
    return JsonResponse(data,safe=False)

# def get_fnb_data(request, fnb_id):
#     fnb = Fnb.objects.get(id=fnb_id)
#     data = {
#         'name': fnb.name,
#         'description': fnb.description,
#         'price': fnb.price,
#     }
#     return JsonResponse(data)

# def edit_fnb_ajax(request, fnb_id):
#     fnb = Fnb.objects.get(id=fnb_id)
#     fnb.name = request.POST.get('name')
#     fnb.description = request.POST.get('description')
#     fnb.price = request.POST.get('price')
#     fnb.save()
#     return HttpResponse(b"UPDATED", status=200)

def edit_fnb(request, id):
    fnb = get_object_or_404(Fnb, id=id)
    if request.method == "POST":
        form = FnbForm(request.POST, instance=fnb)
        if form.is_valid():
            form.save()
            return redirect('ingredient:show_filter')  # Adjust to your post-edit redirect page
    else:
        form = FnbForm(instance=fnb)
    return render(request, 'edit_fnb.html', {'form': form, 'fnb': fnb})

def delete_fnb(request, id):
    fnb = Fnb.objects.get(pk=id)
    fnb.delete()
    return HttpResponseRedirect(reverse('ingredient:show_filter'))


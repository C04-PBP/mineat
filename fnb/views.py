import json
import uuid
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
from django.contrib.auth.models import User


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
        # Use the ingredients field from the model directly as a string
        ingredients_list = i.ingredients if i.ingredients else ""  # Use "" if no ingredients
        data.append({
<<<<<<< HEAD
            "id": i.id,
=======
            "id" : i.id,
>>>>>>> c4902da4c956f3839a5adeff2c19d167db640c40
            "title": i.name,
            "price": i.price,
            "description": i.description,
            "ingredients": ingredients_list,  # Ensure it's a string
            "imageUrl": i.image.url,
        })
    return JsonResponse(data, safe=False)

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
            return redirect('ingredient:show_filter')
    else:
        form = FnbForm(instance=fnb)
    return render(request, 'edit_fnb.html', {'form': form, 'fnb': fnb})

def delete_fnb(request, id):
    fnb = Fnb.objects.get(pk=id)
    fnb.delete()
    return HttpResponseRedirect(reverse('ingredient:show_filter'))

@csrf_exempt
def create_fnb_flutter(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            print("Received data:", data)  # Log the incoming data for debugging
            print(type(data['ingredients']))

            # Generate a random UUID for the id
            random_id = uuid.uuid4()

            # Assign a default user (e.g., the first user in the database)
            default_user = User.objects.first()
            if not default_user:
                return JsonResponse({"status": "error", "message": "No default user found"}, status=500)

            # Create the Fnb object with the UUID and other data
            new_fnb = Fnb.objects.create(
                id=random_id,  # Set the generated UUID as the ID
                name=data["title"],
                image=data["imageUrl"],  # Use the correct key name
                price=data["price"],
                description=data["description"],
                ingredients=data["ingredients"],
                user=default_user  # Assign the default user
            )

            # Return success response
            return JsonResponse({"status": "success", "id": str(random_id)}, status=200)

        except KeyError as e:
            # Handle missing fields in the request body
            print("Missing field in request data:", str(e))
            return JsonResponse({"status": "error", "message": f"Missing field: {str(e)}"}, status=400)
        except Exception as e:
            # Handle other exceptions
            print("Error occurred:", str(e))
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_fnb_flutter(request, id):
    if request.method == 'DELETE':
        try:
            fnb = Fnb.objects.get(id=id)
            fnb.delete()
            return JsonResponse({'message': 'Food item deleted successfully'}, status=200)
        except Fnb.DoesNotExist:
            return JsonResponse({'error': 'Food item not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
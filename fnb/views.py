from django.shortcuts import render, redirect, reverse
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
    return redirect('fnb:login')

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

def add_fnb_ajax(request):
    name = request.POST.get("name")
    description = request.POST.get("description")
    price = request.POST.get("price")
    user = request.user

    new_fnb = Fnb(
        name=name, description=description,
        price=price,
        user=user
    )
    new_fnb.save()

    return HttpResponse(b"CREATED", status=201)

def show_json(request):
    data = Fnb.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
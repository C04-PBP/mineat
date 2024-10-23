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

# Create your views here.
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

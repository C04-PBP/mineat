from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from main.models import Food,Restaurant

# Create your views here.

# JANGAN LUPA MODEL attr review tolong diset kalo lebih dari 5 muncul tetep 5
def show_dashboard(request):
    foods = Food.objects.all()
    restaurants = Restaurant.objects.all()

    context = {
        "foods" : foods,
        "restaurants" : restaurants,
    }

    return render(request,"dashboard.html",context)
from django.urls import path
from restaurant.views import (
    show_restaurant
    )


app_name = 'restaurant'

urlpatterns = [
    path('', show_restaurant, name='show_restaurant'),
]
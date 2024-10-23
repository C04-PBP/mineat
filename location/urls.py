from django.urls import path
from location.views import (
    show_location,get_restaurant
    )


app_name = 'location'

urlpatterns = [
    path('', show_location, name='show_location'),
    path('get_restaurant/', get_restaurant, name='get_restaurant'),
]
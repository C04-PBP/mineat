from django.urls import path
from restaurant.views import show_restaurant, ajax_search_restaurant, ajax_search_district


app_name = 'restaurant'

urlpatterns = [
    path('', show_restaurant, name='show_restaurant'),
    path('search-restaurant/', ajax_search_restaurant, name='ajax_search_restaurant'),
    path('search-district/', ajax_search_district, name='ajax_search_district'), 
]
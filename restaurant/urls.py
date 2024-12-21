from django.urls import path
from restaurant.views import show_restaurant, ajax_search_restaurant, ajax_search_district, ajax_search_fnb
from restaurant.views import restaurant_details, add_restaurant, delete_restaurant, edit_restaurant
from restaurant.views import add_restaurant_ajax,show_json


app_name = 'restaurant'

urlpatterns = [
    path('', show_restaurant, name='show_restaurant'),
    path('search-restaurant/', ajax_search_restaurant, name='ajax_search_restaurant'),
    path('search-district/', ajax_search_district, name='ajax_search_district'),
    path('search-fnb/', ajax_search_fnb, name='ajax_search_fnb'),
    path('restaurant-details/', restaurant_details, name='restaurant_details'),
    path('add-restaurant/', add_restaurant, name='add_restaurant'),
    path('delete/<uuid:id>', delete_restaurant, name='delete_restaurant'),
    path('edit-restaurant/<uuid:id>', edit_restaurant, name='edit_restaurant'),
    path('add-restaurant-ajax/', add_restaurant_ajax, name='add_restaurant_ajax'),
    path('json/', show_json, name="json")
]
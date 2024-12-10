from django.urls import path
from location.views import show_location, location_details, location_search_ajax,show_json
from location.views import update_trivia


app_name = 'location'

urlpatterns = [
    path('', show_location, name='show_location'),
    path('search-location/', location_search_ajax, name='location_search_ajax'),
    path('location-details/', location_details, name='location_details'),
    path('update_trivia/', update_trivia, name='update_trivia'),
    path('json/', show_json, name= "json")
]
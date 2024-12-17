from django.urls import path
from ingredient.views import (
    show_filter,record_ingredients,search_ingredient,show_json
    )


app_name = 'ingredient'

urlpatterns = [
    path('', show_filter, name='show_filter'),
    path('record_ingredients/', record_ingredients, name='record_ingredients'),
    path("search_ingredient/",search_ingredient,name= "search_ingredient"),
    path("json/",show_json, name="json")
]
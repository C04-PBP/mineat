from django.urls import path
from ingredient.views import (
    show_filter,record_ingredients,show_card,search_ingredient
    )


app_name = 'ingredient'

urlpatterns = [
    path('', show_filter, name='show_filter'),
    path('record_ingredients/', record_ingredients, name='record_ingredients'),
    path("product_card/",show_card),
    path("search_ingredient/",search_ingredient,name= "search_ingredient")
]
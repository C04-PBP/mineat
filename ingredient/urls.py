from django.urls import path
from ingredient.views import (
    show_filter,record_ingredients
    )


app_name = 'ingredient'

urlpatterns = [
    path('', show_filter, name='show_filter'),
    path('record_ingredients/', record_ingredients, name='record_ingredients'),
]
from django.urls import path
from fnb.views import (
    show_fnb
    )


app_name = 'fnb'

urlpatterns = [
    path('',show_fnb, name='show-fnb'),
]
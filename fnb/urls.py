from django.urls import path
from fnb.views import (
    show_fnb
    )
from fnb.views import register, login_user, logout_user, ajax_search_fnb, add_fnb


app_name = 'fnb'

urlpatterns = [
    path('',show_fnb, name='show-fnb'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('', ajax_search_fnb, name='ajax_search_fnb'),
    path('add_fnb/', add_fnb, name='add_fnb'),
]

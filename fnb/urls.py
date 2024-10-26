from django.urls import path
from fnb.views import (
    show_fnb
    )
from fnb.views import register, login_user, logout_user, add_fnb, search_fnbs, add_fnb_ajax, show_json


app_name = 'fnb'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_fnb/', add_fnb, name='add_fnb'),
    path('search_fnbs/', search_fnbs, name='search_fnbs'),
    path('add_fnb_ajax/', add_fnb_ajax, name='add_fnb_ajax'),
    path('show_json/', show_json, name='show_json'),
    # path('', landing_page, name='landing_page'),
]

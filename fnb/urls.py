from django.urls import path
from fnb.views import (
    show_fnb
    )
from fnb.views import register, login_user, logout_user


app_name = 'fnb'

urlpatterns = [
    path('',show_fnb, name='show-fnb'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
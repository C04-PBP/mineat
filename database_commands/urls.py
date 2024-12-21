from django.urls import path
from database_commands.views import (
    login_flutter,logout_flutter,register_flutter)


app_name = 'flutter'

urlpatterns = [
    path('login/', login_flutter, name='login_flutter'),
    path('logout/',logout_flutter, name="logout_flutter"),
    path('register/',register_flutter, name='register_flutter')
]
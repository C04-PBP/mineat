from django.urls import path
from fnb.views import (
    show_fnb
    )
from fnb.views import register, login_user, logout_user, add_fnb, search_fnbs, add_fnb_ajax, show_json, edit_fnb, delete_fnb


app_name = 'fnb'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_fnb/', add_fnb, name='add_fnb'),
    path('search_fnbs/', search_fnbs, name='search_fnbs'),
    path('add_fnb_ajax/', add_fnb_ajax, name='add_fnb_ajax'),
    path('show_json/', show_json, name='show_json'),
    # path('get_fnb_data/<int:fnb_id>/', get_fnb_data, name='get_fnb_data'),
    # path('edit_fnb_ajax/<int:fnb_id>/', edit_fnb_ajax, name='edit_fnb_ajax'),
    path('fnb/edit_fnb/<uuid:id>/', edit_fnb, name='edit_fnb'),
    path('fnb/delete_fnb/<uuid:id>/', delete_fnb, name='delete_fnb')
    # path('', landing_page, name='landing_page'),
]

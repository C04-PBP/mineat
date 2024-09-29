from django.urls import path
from main.views import (
    show_dashboard
)

urlpatterns = [
    path('', show_dashboard , name="dashboard"),
]

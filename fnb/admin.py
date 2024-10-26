from django.contrib import admin
from .models import Fnb


# Register your models here.

@admin.register(Fnb)
class FnbAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image')  # Fields to display in the list view
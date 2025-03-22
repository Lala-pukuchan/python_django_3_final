from django.contrib import admin

# Register your models here.
# chat/admin.py
from .models import Room

admin.site.register(Room)

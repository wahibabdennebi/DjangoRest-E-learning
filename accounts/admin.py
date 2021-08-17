from django.contrib import admin

# Register your models here.
from .models import Abonne
from rest_framework_simplejwt import token_blacklist







class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','created_at']


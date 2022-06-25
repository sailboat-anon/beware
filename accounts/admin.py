from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'website']

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['user']
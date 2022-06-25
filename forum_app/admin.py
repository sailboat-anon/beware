from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'id', 'is_thread', 'created_at']
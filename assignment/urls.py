from django.urls import path
from .views import *

urlpatterns = [
    path('', browse, name='MIDST'),
    path('tasks', tasks, name='tasks'),
    ]
    
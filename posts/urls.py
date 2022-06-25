from django.urls import path
from . import views
from django.contrib.auth import views as dv

urlpatterns = [
    path('new', views.new_post, name='newpost'),
    path('vote', views.vote, name='vote'),
    path('<str:post_id>', views.post_view)
]
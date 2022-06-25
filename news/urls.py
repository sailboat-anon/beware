from django.urls import path
from .views import NewArticle, ArticleSubmit

urlpatterns = [
    path('new', NewArticle, name='new_article'),
    path('submit', ArticleSubmit),
    ]
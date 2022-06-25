from django.urls import path
from . import views
from django.contrib.auth import views as dv


urlpatterns = [
    path('login', views.user_login, name='login'),
    path('logout', dv.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('change_password', dv.PasswordChangeView.as_view(), name='password_change'),
    path('password_changed', dv.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', dv.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', dv.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', dv.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', dv.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('edit', views.edit, name='edit'),
    path('settings', views.settings, name='settings'),
]
from django.shortcuts import redirect
from django.urls import path, reverse

from apps.users import views

app_name = 'users'

urlpatterns = [
    path('perfil/', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/', lambda r: redirect(reverse('users:profile'))),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

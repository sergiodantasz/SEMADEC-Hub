from django.shortcuts import redirect
from django.urls import path, reverse

from users.views import login, logout, profile

app_name = 'users'

urlpatterns = [
    path('perfil/', profile, name='profile'),
    path('accounts/profile/', lambda r: redirect(reverse('users:profile'))),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]

from django.urls import path

from users.views import login

app_name = 'users'

urlpatterns = [
    path('perfil/', lambda request: '<h1>TEST</h1>', name='profile'),
    path('login/', login, name='login'),
    path('logout/', lambda request: '<h1>TEST</h1>', name='logout'),
]

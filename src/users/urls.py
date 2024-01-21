from django.urls import path

app_name = 'users'

urlpatterns = [
    path('perfil/', lambda request: '<h1>TEST</h1>', name='perfil'),
    path('login/', lambda request: '<h1>TEST</h1>', name='login'),
    path('logout/', lambda request: '<h1>TEST</h1>', name='logout'),
]

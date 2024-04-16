from django.urls import path

from editions import views

app_name = 'editions'

urlpatterns = [
    path('', views.editions, name='editions'),
    path('criar', views.editions_create, name='editions_create'),
]

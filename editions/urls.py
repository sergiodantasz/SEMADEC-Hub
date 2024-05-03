from django.urls import path

from editions import views

app_name = 'editions'

urlpatterns = [
    path('', views.editions, name='editions'),
    path('criar/', views.editions_create, name='editions_create'),
    path('buscar/', views.editions_search, name='editions_search'),
    path('visualizar/<int:pk>/', views.editions_detailed, name='editions_detailed'),
    path('editar/<int:year>/', views.editions_edit, name='editions_edit'),
    path('apagar/<int:year>/', views.editions_delete, name='editions_delete'),
]

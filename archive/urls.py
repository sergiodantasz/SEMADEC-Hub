from django.urls import path

from archive import views

app_name = 'archive'

urlpatterns = [
    path('', views.archive, name='archive'),
    path('adicionar/', views.submit_archive, name='submitarchive'),
    path('adicionar/criar/', views.create_archive, name='createarchive'),
]

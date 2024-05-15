from django.urls import path

from archive import views

app_name = 'archive'

urlpatterns = [
    path('', views.archive_collection, name='archive'),
    path('criar/', views.create_archive_collection, name='create_archive'),
    path('visualizar/<slug:slug>/', views.view_archive_collection, name='view_archive'),
    path('apagar/<slug:slug>/', views.delete_archive_collection, name='delete_archive'),
    path('editar/<slug:slug>/', views.edit_archive_collection, name='edit_archive'),
    path('imagem/apagar/<int:pk>/', views.delete_image, name='delete_image'),
]

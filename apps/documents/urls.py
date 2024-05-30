from django.urls import path

from apps.documents import views

app_name = 'documents'

urlpatterns = [
    path('', views.documents_collection, name='documents'),
    path('criar/', views.create_document_collection, name='create_document'),
    path(
        'apagar/<slug:slug>/', views.delete_document_collection, name='delete_document'
    ),
    path('buscar/', views.search_document_collection, name='search_document'),
    # path('editar/<slug:slug>/', views.edit_document_collection, name='edit_document'),
]

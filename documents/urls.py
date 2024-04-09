from django.urls import path

from documents import views

app_name = 'documents'

urlpatterns = [
    path('', views.documents_collection, name='documents'),
    path('apagar/', views.create_document_collection, name='create_document'),
    path(
        'remover/<slug:slug>/', views.delete_document_collection, name='delete_document'
    ),
    path('buscar/', views.search_document_collection, name='search_document'),
]

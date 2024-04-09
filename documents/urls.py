from django.urls import path

from documents import views

app_name = 'documents'

urlpatterns = [
    path('', views.documents_collection, name='documents'),
    path('create/', views.create_document_collection, name='create_document'),
    path(
        'delete/<slug:slug>/', views.delete_document_collection, name='delete_document'
    ),
]

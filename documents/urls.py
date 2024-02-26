from django.urls import path

from documents import views

app_name = 'documents'

urlpatterns = [
    path('', views.documents, name='documents'),
]

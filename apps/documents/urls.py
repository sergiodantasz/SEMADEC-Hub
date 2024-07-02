from django.urls import path

from apps.documents import views

app_name = 'documents'

urlpatterns = [
    path('', views.DocumentListView.as_view(), name='home'),
    path('criar/', views.DocumentCreateView.as_view(), name='create'),
    path('apagar/<slug:slug>/', views.DocumentDeleteView.as_view(), name='delete'),
    path('buscar/', views.DocumentSearchView.as_view(), name='search'),
    path('editar/<slug:slug>/', views.DocumentEditView.as_view(), name='edit'),
]

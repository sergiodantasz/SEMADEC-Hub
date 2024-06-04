from django.urls import path

from apps.news import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('buscar/', views.NewsSearchListView.as_view(), name='search'),
    path('criar/', views.NewsCreateView.as_view(), name='create'),
    path('apagar/<slug:slug>/', views.NewsDeleteView.as_view(), name='delete'),
    path('editar/<slug:slug>/', views.NewsEditView.as_view(), name='edit'),
    path('visualizar/<slug:slug>/', views.NewsDetailView.as_view(), name='view'),
]

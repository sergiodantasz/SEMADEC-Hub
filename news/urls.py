from django.urls import path

from news import views

app_name = 'news'

urlpatterns = [
    path('', views.news, name='news'),
    path('criar/', views.create_news, name='create_news'),
    path('apagar/<slug:slug>/', views.delete_news, name='delete_news'),
    path('editar/<slug:slug>/', views.edit_news, name='edit_news'),
    path('visualizar/<slug:slug>/', views.view_news, name='view_news'),
]

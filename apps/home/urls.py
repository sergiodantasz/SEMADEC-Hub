from django.urls import path

from apps.home import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tags/', views.tags, name='tags'),
    path('tags/criar/', views.tags_create, name='tags_create'),
    path('tags/apagar/<slug:slug>/', views.tags_delete, name='tags_delete'),
]

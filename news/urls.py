from django.urls import path

from news import views

app_name = 'news'

urlpatterns = [
    path('', views.news, name='news'),
    path('criar/', views.create_news, name='create_news'),
]

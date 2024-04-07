from django.urls import path

from competitions import views

app_name = 'competitions'


urlpatterns = [
    path('', views.competitions, name='competitions'),
    path('esportes/', views.sports, name='sports'),
    path('esportes/busca', views.sports_search, name='sports_search'),
    path('provas/', views.tests, name='tests'),
    path('provas/busca', views.tests_search, name='tests_search'),
]

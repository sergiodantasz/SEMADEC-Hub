from django.urls import path

from competitions import views

app_name = 'competitions'


urlpatterns = [
    path('', views.competitions, name='competitions'),
    path('esportes/', views.sports, name='sports'),
    path('esportes/buscar', views.sports_search, name='sports_search'),
    path('esportes/criar', views.sports_create, name='sports_create'),
    path('provas/', views.tests, name='tests'),
    path('provas/buscar', views.tests_search, name='tests_search'),
    path('provas/criar', views.tests_create, name='tests_create'),
]

from django.urls import path

from competitions import views

app_name = 'competitions'


urlpatterns = [
    path('', views.competitions, name='competitions'),
    path('esportes/', views.sports, name='sports'),
    path(
        'esportes/partidas/criar/<int:pk>/',
        views.matches_create,
        name='matches_create',
    ),
    path(
        'esportes/partidas/editar/<int:pk>/',
        views.matches_edit,
        name='matches_edit',
    ),
    path(
        'esportes/visualizar/<slug:slug>/',
        views.sports_detailed,
        name='sports_detailed',
    ),
    path('esportes/buscar', views.sports_search, name='sports_search'),
    path('esportes/criar', views.sports_create, name='sports_create'),
    path('esportes/editar/<slug:slug>/', views.sports_edit, name='sports_edit'),
    path('provas/', views.tests, name='tests'),
    path('provas/buscar', views.tests_search, name='tests_search'),
    path('provas/criar', views.tests_create, name='tests_create'),
    path('provas/editar/<slug:slug>/', views.tests_edit, name='tests_edit'),
]

from django.urls import include, path

from apps.competitions import views

app_name = 'competitions'

matches_urls = (
    [
        path('criar/<int:pk>/', views.matches_create, name='create'),
        path('editar/<int:pk>/', views.matches_edit, name='edit'),
    ],
    'matches',
)

sports_urls = (
    [
        path('', views.sports, name='home'),
        path('visualizar/<slug:slug>/', views.sports_detailed, name='detailed'),
        path('criar', views.sports_create, name='create'),
        path('buscar', views.sports_search, name='search'),
        path('editar/<slug:slug>/', views.sports_edit, name='edit'),
        path('apagar/<slug:slug>/', views.sports_delete, name='delete'),
        path('partidas/', include(matches_urls)),
    ],
    'sports',
)

tests_urls = (
    [
        path('', views.tests, name='home'),
        path('visualizar/<slug:slug>/', views.tests_detailed, name='detailed'),
        path('criar', views.tests_create, name='create'),
        path('buscar', views.tests_search, name='search'),
        path('editar/<slug:slug>/', views.tests_edit, name='edit'),
        path('apagar/<slug:slug>/', views.tests_delete, name='delete'),
    ],
    'tests',
)

urlpatterns = [
    path('', views.competitions, name='home'),
    path('esportes/', include(sports_urls)),
    path('provas/', include(tests_urls)),
]

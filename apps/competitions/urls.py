from django.urls import include, path

from apps.competitions import views

app_name = 'competitions'

matches_urls = (
    [
        path('criar/<int:pk>/', views.MatchCreateView.as_view(), name='create'),
        path('editar/<int:pk>/', views.MatchEditView.as_view(), name='edit'),
    ],
    'matches',
)

sports_urls = (
    [
        path('', views.SportListView.as_view(), name='home'),
        path(
            'visualizar/<slug:slug>/',
            views.SportDetailedView.as_view(),
            name='detailed',
        ),
        path('criar', views.SportCreateView.as_view(), name='create'),
        path('buscar', views.SportSearchView.as_view(), name='search'),
        path('editar/<slug:slug>/', views.SportEditView.as_view(), name='edit'),
        path('apagar/<slug:slug>/', views.SportDeleteView.as_view(), name='delete'),
        path('partidas/', include(matches_urls)),
    ],
    'sports',
)

tests_urls = (
    [
        path('', views.TestListView.as_view(), name='home'),
        path(
            'visualizar/<slug:slug>/', views.TestDetailedView.as_view(), name='detailed'
        ),
        path('criar', views.TestCreateView.as_view(), name='create'),
        path('buscar', views.TestSearchView.as_view(), name='search'),
        path('editar/<slug:slug>/', views.TestEditView.as_view(), name='edit'),
        path('apagar/<slug:slug>/', views.TestDeleteView.as_view(), name='delete'),
    ],
    'tests',
)

urlpatterns = [
    path('', views.CompetitionView.as_view(), name='home'),
    path('esportes/', include(sports_urls)),
    path('provas/', include(tests_urls)),
]

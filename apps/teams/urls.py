from django.urls import include, path

from apps.teams import views

app_name = 'teams'

classes_urls = (
    [
        path('', views.classes, name='home'),
        path('criar/', views.classes_create, name='create'),
        path('buscar/', views.classes_search, name='search'),
        path('editar/<slug:slug>/', views.classes_edit, name='edit'),
        path('apagar/<slug:slug>/', views.classes_delete, name='delete'),
    ],
    'classes',
)

courses_urls = (
    [
        path('', views.courses, name='home'),
        path('criar/', views.courses_create, name='create'),
        path('buscar/', views.courses_search, name='search'),
        path('editar/<slug:slug>/', views.courses_edit, name='edit'),
        path('apagar/<slug:slug>/', views.courses_delete, name='delete'),
    ],
    'courses',
)

urlpatterns = [
    path('', views.teams, name='home'),
    path('criar/', views.teams_create, name='create'),
    path('buscar/', views.teams_search, name='search'),
    path('editar/<slug:slug>/', views.teams_edit, name='edit'),
    path('apagar/<slug:slug>/', views.teams_delete, name='delete'),
    path('turmas/', include(classes_urls)),
    path('cursos/', include(courses_urls)),
]

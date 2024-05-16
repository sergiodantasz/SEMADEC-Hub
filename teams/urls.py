from django.urls import path

from teams import views

app_name = 'teams'

urlpatterns = [
    # Teams
    path('', views.teams, name='teams'),
    path('criar/', views.teams_create, name='teams_create'),
    path('buscar/', views.teams_search, name='teams_search'),
    path('editar/<slug:slug>/', views.teams_edit, name='teams_edit'),
    path('apagar/<slug:slug>/', views.teams_delete, name='teams_delete'),
    # Classes
    path('turmas/', views.classes, name='classes'),
    path('turmas/criar/', views.classes_create, name='classes_create'),
    path('turmas/buscar/', views.classes_search, name='classes_search'),
    path('turmas/editar/<slug:slug>/', views.classes_edit, name='classes_edit'),
    path('turmas/apagar/<slug:slug>/', views.classes_delete, name='classes_delete'),
    # Courses
    path('cursos/', views.courses, name='courses'),
    path('cursos/criar/', views.courses_create, name='courses_create'),
    path('cursos/buscar/', views.courses_search, name='courses_search'),
    path('cursos/editar/<slug:slug>/', views.courses_edit, name='courses_edit'),
    path('cursos/apagar/<slug:slug>/', views.courses_delete, name='courses_delete'),
]

from django.urls import include, path

from apps.teams import views

app_name = 'teams'

classes_urls = (
    [
        path('', views.ClassListView.as_view(), name='home'),
        path('criar/', views.ClassCreateView.as_view(), name='create'),
        path('buscar/', views.ClassSearchView.as_view(), name='search'),
        path('editar/<slug:slug>/', views.ClassEditView.as_view(), name='edit'),
        path('apagar/<slug:slug>/', views.ClassDeleteView.as_view(), name='delete'),
    ],
    'classes',
)

courses_urls = (
    [
        path('', views.CourseListView.as_view(), name='home'),
        path('buscar/', views.CourseSearchView.as_view(), name='search'),
        path('criar/', views.CourseCreateView.as_view(), name='create'),
        path('editar/<slug:slug>/', views.CourseEditView.as_view(), name='edit'),
        path('apagar/<slug:slug>/', views.CourseDeleteView.as_view(), name='delete'),
    ],
    'courses',
)

urlpatterns = [
    path('', views.TeamView.as_view(), name='home'),
    path('criar/', views.TeamCreateView.as_view(), name='create'),
    path('buscar/', views.TeamSearchView.as_view(), name='search'),
    path('editar/<slug:slug>/', views.TeamEditView.as_view(), name='edit'),
    path('apagar/<slug:slug>/', views.TeamDeleteView.as_view(), name='delete'),
    path('turmas/', include(classes_urls)),
    path('cursos/', include(courses_urls)),
]

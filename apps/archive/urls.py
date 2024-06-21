from django.urls import include, path

from apps.archive import views

app_name = 'archive'

image_urls = (
    [
        path('apagar/<int:pk>/', views.ArchiveImageDeleteView.as_view(), name='delete'),
    ],
    'image',
)

urlpatterns = [
    path('', views.ArchiveListView.as_view(), name='home'),
    path('criar/', views.ArchiveCreateView.as_view(), name='create'),
    path('buscar/', views.ArchiveSearchView.as_view(), name='search'),
    path('visualizar/<slug:slug>/', views.ArchiveDetailView.as_view(), name='detail'),
    path('editar/<slug:slug>/', views.ArchiveEditView.as_view(), name='edit'),
    path('apagar/<slug:slug>/', views.ArchiveDeleteView.as_view(), name='delete'),
    path('imagem/', include(image_urls)),
]

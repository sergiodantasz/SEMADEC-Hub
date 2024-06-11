from django.urls import include, path

from apps.archive import views

app_name = 'archive'

image_urls = (
    [
        path('apagar/<int:pk>/', views.delete_image, name='delete'),
    ],
    'image',
)

urlpatterns = [
    path('', views.ArchiveListView.as_view(), name='list'),
    path('criar/', views.create_archive_collection, name='create'),
    # path('buscar/', views.search_archive_collection, name='search'),
    path('visualizar/<slug:slug>/', views.ArchiveDetailView.as_view(), name='detail'),
    path('editar/<slug:slug>/', views.edit_archive_collection, name='edit'),
    path('apagar/<slug:slug>/', views.delete_archive_collection, name='delete'),
    path('imagem/', include(image_urls)),
]

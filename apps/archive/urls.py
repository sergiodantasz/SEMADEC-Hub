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
    path('', views.archive_collection, name='home'),
    path('criar/', views.create_archive_collection, name='create'),
    # path('buscar/', views.search_archive_collection, name='search'),
    path('visualizar/<slug:slug>/', views.view_archive_collection, name='detailed'),
    path('editar/<slug:slug>/', views.edit_archive_collection, name='edit'),
    path('apagar/<slug:slug>/', views.delete_archive_collection, name='delete'),
    path('imagem/', include(image_urls)),
]

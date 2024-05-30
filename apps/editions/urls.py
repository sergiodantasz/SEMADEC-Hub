from django.urls import path

from apps.editions import views

app_name = 'editions'

urlpatterns = [
    path('', views.EditionView.as_view(), name='editions'),
    path('criar/', views.EditionCreateFormView.as_view(), name='editions_create'),
    path('buscar/', views.EditionSearchView.as_view(), name='editions_search'),
    path(
        'visualizar/<int:pk>/',
        views.EditionDetailedView.as_view(),
        name='editions_detailed',
    ),
    path('editar/<int:pk>/', views.EditionEditFormView.as_view(), name='editions_edit'),
    path('apagar/<int:pk>/', views.EditionDeleteView.as_view(), name='editions_delete'),
]

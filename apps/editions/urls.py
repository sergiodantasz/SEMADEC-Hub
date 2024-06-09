from django.urls import path

from apps.editions import views

app_name = 'editions'

urlpatterns = [
    path('', views.EditionListView.as_view(), name='home'),
    path('criar/', views.EditionCreateView.as_view(), name='create'),
    path('buscar/', views.EditionSearchView.as_view(), name='search'),
    path(
        'visualizar/<int:pk>/',
        views.EditionDetailView.as_view(),
        name='detailed',
    ),
    path('editar/<int:pk>/', views.EditionEditView.as_view(), name='edit'),
    path('apagar/<int:pk>/', views.EditionDeleteView.as_view(), name='delete'),
]

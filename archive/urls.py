from django.urls import path

from archive import views

app_name = 'archive'

urlpatterns = [
    path('', views.archive, name='archive'),
    path('<slug:slug>/', views.archive_detailed, name='archive_detailed'),
    path('adicionar/', views.submit_archive, name='submitarchive'),
    path('adicionar/criar/', views.create_archive, name='createarchive'),
]

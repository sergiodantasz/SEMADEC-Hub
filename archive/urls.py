from django.urls import path

from archive import views

app_name = 'archive'

urlpatterns = [
    path('', views.archive, name='archive'),
    path('<slug:slug>/', views.archive_detailed, name='archive_detailed'),
]

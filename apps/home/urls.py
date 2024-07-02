from django.urls import include, path

from apps.home import views

app_name = 'home'
tags_urls = (
    [
        path('', views.tags, name='home'),
        path('criar/', views.tags_create, name='create'),
        path('apagar/<slug:slug>/', views.tags_delete, name='delete'),
    ],
    'tags',
)
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tags/', include(tags_urls)),
]

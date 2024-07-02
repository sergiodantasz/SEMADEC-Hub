from django.urls import include, path

from apps.home import views

app_name = 'home'
tags_urls = (
    [
        path('', views.TagListView.as_view(), name='home'),
        path('criar/', views.TagCreateView.as_view(), name='create'),
        path('apagar/<slug:slug>/', views.TagDeleteView.as_view(), name='delete'),
    ],
    'tags',
)
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tags/', include(tags_urls)),
]

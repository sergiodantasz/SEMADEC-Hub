from django.urls import path

app_name = 'news'

urlpatterns = [
    path('', lambda request: '<h1>TEST</h1>', name='news'),
]

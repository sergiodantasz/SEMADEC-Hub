from django.urls import path

app_name = 'archive'

urlpatterns = [
    path('', lambda request: '<h1>TEST</h1>', name='archive'),
]

from django.urls import path

app_name = 'editions'

urlpatterns = [
    path('', lambda request: '<h1>TEST</h1>', name='editions'),
]

from django.urls import path

app_name = 'competitions'

urlpatterns = [
    path('', lambda request: '<h1>TEST</h1>', name='competitions'),
]

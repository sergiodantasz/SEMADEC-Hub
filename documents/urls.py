from django.urls import path

app_name = 'documents'

urlpatterns = [
    path('', lambda request: '<h1>TEST</h1>', name='documents'),
]

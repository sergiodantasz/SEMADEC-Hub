from django.urls import path

app_name = 'home'

urlpatterns = [
    path('', lambda request: '<h1>TEST</h1>', name='home'),
]

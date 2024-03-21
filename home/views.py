from django.shortcuts import render


def home(request):
    context = {'title': 'Início'}
    return render(request, 'home/pages/home.html', context)

from django.shortcuts import render


def competitions(request):
    context = {'title': 'Competições'}
    return render(request, 'competitions/pages/competitions.html', context)

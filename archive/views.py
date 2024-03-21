from django.shortcuts import render


def archive(request):
    context = {'title': 'Acervo'}
    return render(request, 'archive/pages/archive.html', context)

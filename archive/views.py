from django.shortcuts import render


def archive(request):
    return render(
        request,
        'archive/pages/archive.html',
        context={'title': 'Acervo - SEMADECHub'},
    )

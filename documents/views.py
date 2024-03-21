from django.shortcuts import render


def documents(request):
    context = {'title': 'Documentos'}
    return render(request, 'documents/pages/documents.html', context)

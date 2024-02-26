from django.shortcuts import render

from users.models import User


def documents(request):
    context = {'title': 'Documentos'}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
    return render(request, 'documents/pages/documents.html', context)

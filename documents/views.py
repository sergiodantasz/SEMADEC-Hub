from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from archive.tests.factories import CollectionDocumentsFactory, DocumentFactory
from users.models import User


@login_required(login_url='/login/')
def documents(request):
    context = {'title': 'Documentos'}
    document_regs = CollectionDocumentsFactory.create_batch(
        size=3,
        files=(
            DocumentFactory(),
            DocumentFactory(),
            DocumentFactory(display_name=''),
        ),
    )
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
        context['document_regs'] = document_regs
    return render(request, 'documents/pages/documents.html', context)

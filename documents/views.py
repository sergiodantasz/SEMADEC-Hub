from django.shortcuts import render

from archive.tests.factories import CollectionDocumentsFactory, DocumentFactory
from home.tests.factories import TagFactory


def documents(request):
    context = {'title': 'Documentos'}
    files = DocumentFactory.create_batch(3)
    tags = TagFactory.create_batch(3)
    document_regs = CollectionDocumentsFactory.create_batch(
        size=3,
        files=files,
        tags=tags,
    )
    context['document_regs'] = document_regs
    return render(request, 'documents/pages/documents.html', context)

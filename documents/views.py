from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse

from archive.models import Collection
from archive.tests.factories import CollectionDocumentsFactory, DocumentFactory
from home.tests.factories import TagFactory


def documents(request):
    files = DocumentFactory.create_batch(3)
    tags = TagFactory.create_batch(3)
    document_regs = CollectionDocumentsFactory.create_batch(
        size=3,
        files=files,
        tags=tags,
    )  # Remove if needed
    context = {
        'title': 'Documentos',
        'page_content': Collection.objects.filter(collection_type='document').order_by(
            'created_at'
        ),
        'search_namespace': reverse('documents:documents_search'),
    }

    return render(request, 'documents/pages/documents.html', context)


def documents_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        return redirect(reverse('documents:documents'))

    search_output = Collection.objects.filter(
        Q(
            Q(collection_type__iexact='document')
            & Q(
                Q(title__icontains=querystr),
            )
        ),
    )
    context = {
        'title': 'Documentos',
        'page_content': search_output,
    }
    return render(request, 'documents/pages/documents.html', context)

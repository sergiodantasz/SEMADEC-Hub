from django.shortcuts import get_object_or_404, render

from archive.tests.factories import CollectionArchiveFactory, ImageFactory
from home.models import Collection


def archive(request):
    # For test purposes
    collection_fac = CollectionArchiveFactory()
    document_fac = ImageFactory.create_batch(
        size=3,
        collection=collection_fac,
    )
    archive_regs = [collection_fac] * 5
    # For test purposes
    context = {'title': 'Acervo', 'archive_regs': archive_regs}
    return render(request, 'archive/pages/archive.html', context)


def archive_detailed(request, slug):
    archive = get_object_or_404(Collection, slug=slug)
    context = {'title': archive.title, 'archive_reg': archive}
    return render(request, 'archive/pages/archive_detailed.html', context)

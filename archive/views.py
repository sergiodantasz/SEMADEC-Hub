from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from archive.forms import SubmitArchiveForm
from archive.models import Collection
from archive.tests.factories import (
    CollectionArchiveFactory,
    ImageFactory,
)


def archive(request):
    archive_regs = CollectionArchiveFactory.create_batch(
        size=3,
        files=(
            ImageFactory(),
            ImageFactory(),
            ImageFactory(),
        ),
    )
    context = {
        'title': 'Acervo',
        'archive_regs': archive_regs,
    }
    return render(request, 'archive/pages/archive.html', context)


def archive_detailed(request, slug):
    archive = get_object_or_404(Collection, slug=slug)
    context = {'title': archive.title, 'archive_reg': archive}
    return render(request, 'archive/pages/archive_detailed.html', context)


def submit_archive(request):  # Change name to `archive_submit`
    form = SubmitArchiveForm()
    context = {'title': 'Acervo', 'form': form}
    return render(request, 'archive/pages/submitarchive.html', context)


def create_archive(request):  # Change name to `archive_create`
    if not request.POST:
        raise Http404()
    form = SubmitArchiveForm(request.POST)
    context = {'title': 'Acervo', 'form': form}
    return render(request, 'archive/pages/submitarchive.html', context)

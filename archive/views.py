from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from archive.models import Collection
from archive.tests.factories import (
    CollectionArchiveFactory,
    ImageFactory,
)
from users.models import User

from .forms import SubmitArchiveForm


def archive(request):
    context = {'title': 'Acervo'}
    archive_regs = CollectionArchiveFactory.create_batch(
        size=3,
        files=(
            ImageFactory(),
            ImageFactory(),
            ImageFactory(),
        ),
    )
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
        context['archive_regs'] = archive_regs
    return render(request, 'archive/pages/archive.html', context)


def archive_detailed(request, slug):
    archive = get_object_or_404(Collection, slug=slug)
    context = {'title': archive.title, 'archive_reg': archive}

    return render(request, 'archive/pages/archive_detailed.html', context)


def submit_archive(request):
    form = SubmitArchiveForm()
    context = {'title': 'Acervo', 'form': form}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
    return render(
        request,
        'archive/pages/submitarchive.html',
        context,
    )


def create_archive(request):
    if not request.POST:
        raise Http404()
    form = SubmitArchiveForm(request.POST)
    context = {'title': 'Acervo', 'form': form}
    if request.user.is_authenticated:
        user = User.objects.get(registration=request.user.username)
        context['user'] = user  # type: ignore
    return render(
        request,
        'archive/pages/submitarchive.html',
        context,
    )

from django.shortcuts import render

from archive.tests.factories import (
    CollectionArchiveFactory,
    ImageFactory,
)
from users.models import User


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

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render

from home.models import Collection


def archive(request):
    context = {
        'title': 'Acervo',
    }
    return render(request, 'archive/pages/archive.html', context)

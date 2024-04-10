from random import choices

from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse

from competitions.models import Sport, Test
from competitions.tests.factories import CategoryFactory, SportFactory, TestFactory


def competitions(request):
    return redirect(reverse('competitions:sports'))


def sports(request):
    cats = CategoryFactory.create_batch(size=3)  # Remove if needed
    SportFactory.create_batch(size=4, categories=choices(cats))  # Remove if needed
    context = {
        'title': 'Competições',
        'page_variant': 'sports',
        'db_regs': Sport.objects.all(),
        'search_url': reverse('competitions:sports_search'),
    }
    return render(request, 'competitions/pages/competitions.html', context)


def sports_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        return redirect(reverse('competitions:sports'))

    db_regs = Sport.objects.filter(name__icontains=querystr).order_by('name')
    context = {
        'title': 'Competições',
        'page_variant': 'sports',
        'db_regs': db_regs,
    }
    return render(request, 'competitions/pages/competitions.html', context)


def tests(request):
    TestFactory.create_batch(size=4)  # Remove if needed
    context = {
        'title': 'Competições',
        'page_variant': 'tests',
        'db_regs': Test.objects.all(),
        'search_url': reverse('competitions:tests_search'),
    }
    return render(request, 'competitions/pages/competitions.html', context)


def tests_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        return redirect(reverse('competitions:tests'))

    db_regs = Test.objects.filter(
        Q(Q(title__icontains=querystr) | Q(description__icontains=querystr))
    ).order_by('title')
    context = {
        'title': 'Competições',
        'page_variant': 'tests',
        'db_regs': db_regs,
    }
    return render(request, 'competitions/pages/competitions.html', context)

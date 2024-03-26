from random import choices

from django.shortcuts import redirect, render
from django.urls import reverse

from competitions.tests.factories import CategoryFactory, SportFactory


def competitions(request):
    return redirect(reverse('competitions:sports'))


def sports(request):
    context = {'title': 'Competições'}
    cats = CategoryFactory.create_batch(size=3)
    sport_regs = SportFactory.create_batch(
        size=4,
        categories=choices(cats, k=1),
    )
    context['competition_type'] = 'sports'
    context['sport_regs'] = sport_regs
    return render(request, 'competitions/pages/competitions.html', context)


def tests(request):
    context = {'title': 'Competições'}
    context['competition_type'] = 'tests'
    return render(request, 'competitions/pages/competitions.html', context)

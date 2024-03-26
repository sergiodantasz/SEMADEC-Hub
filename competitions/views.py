from random import choices

from django.shortcuts import redirect, render
from django.urls import reverse
from factory.django import mute_signals

from competitions.models import Category
from competitions.tests.factories import CategoryFactory, SportFactory


def competitions(request):
    return redirect(reverse('competitions:sports'))


def sports(request):
    context = {'title': 'Competições'}
    # categories = CategoryFactory.generate_batch(
    #     strategy='create',
    #     size=2,
    # )
    cat1 = CategoryFactory()
    cat2 = CategoryFactory()
    # categories = CategoryFactory.create_batch(size=2)
    sport_regs = SportFactory.create_batch(
        size=4,
        categories=[cat1, cat2],
    )
    context['competition_type'] = 'sports'
    context['sport_regs'] = sport_regs
    return render(request, 'competitions/pages/competitions.html', context)


def tests(request):
    context = {'title': 'Competições'}
    context['competition_type'] = 'tests'
    return render(request, 'competitions/pages/competitions.html', context)

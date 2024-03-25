from random import choices

from django.shortcuts import redirect, render
from django.urls import reverse

from competitions.models import Category
from competitions.tests.conftest import category_fixture, sport_with_categories_fixture
from competitions.tests.factories import CategoryFactory, SportFactory


def competitions(request):
    return redirect(reverse('competitions:sports'))


def sports(request):
    context = {'title': 'Competições'}
    # categories = [category_fixture(), category_fixture(), category_fixture()]
    # sport_regs = SportFactory.build_batch(
    #     size=3,
    #     categories=(choices(categories)),
    # )
    # sport_regs = SportFactory(strategy='build', categories=(choices(categories)))
    # sport_regs = SportFactory.create(categories=(choices(categories)))
    # sport_regs = sport_with_categories_fixture()
    context['competition_type'] = 'sports'
    # context['sport_regs'] = sport_regs
    return render(request, 'competitions/pages/competitions.html', context)


def tests(request):
    context = {'title': 'Competições'}
    context['competition_type'] = 'tests'
    return render(request, 'competitions/pages/competitions.html', context)

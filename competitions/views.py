from random import choices

from django.shortcuts import redirect, render
from django.urls import reverse

from competitions.tests.factories import CategoryFactory, SportFactory, TestFactory


def competitions(request):
    return redirect(reverse('competitions:sports'))


def sports(request):
    context = {'title': 'Competições'}
    cats = CategoryFactory.create_batch(size=3)
    competition_regs = SportFactory.create_batch(
        size=4,
        categories=choices(cats, k=1),
    )
    context['competition_type'] = 'sports'
    context['competition_regs'] = competition_regs
    return render(request, 'competitions/pages/competitions.html', context)


def tests(request):
    context = {'title': 'Competições'}
    competition_regs = TestFactory.create_batch(size=4)
    context['competition_type'] = 'tests'
    context['competition_regs'] = competition_regs
    return render(request, 'competitions/pages/competitions.html', context)

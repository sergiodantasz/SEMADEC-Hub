from django.shortcuts import redirect, render
from django.urls import reverse

from competitions.tests.factories import SportFactory


def competitions(request):
    return redirect(reverse('competitions:sports'))


def sports(request):
    context = {'title': 'Competições'}
    context['sport_regs'] = SportFactory.build_batch(3)
    context['competition_type'] = 'sports'
    return render(request, 'competitions/pages/competitions.html', context)


def tests(request):
    context = {'title': 'Competições'}
    context['competition_type'] = 'tests'
    return render(request, 'competitions/pages/competitions.html', context)

from random import choices

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse

from competitions.models import Sport, Test
from competitions.tests.factories import CategoryFactory, SportFactory, TestFactory
from editions.models import Team
from editions.tests.factories import TeamFactory
from helpers.decorators import admin_required

from .forms import SportForm, TestForm


def competitions(request):
    return redirect(reverse('competitions:sports'))


def sports(request):
    # cats = CategoryFactory.create_batch(size=3)  # Remove if needed
    # SportFactory.create_batch(size=1, categories=choices(cats))  # Remove if needed
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


@login_required
@admin_required
def sports_create(request):
    CategoryFactory.create_batch(size=3)  # Remove if needed

    form = SportForm(request.POST or None, request.FILES or None)
    context = {
        'title': 'Criar esporte',
        'form': form,
        'form_action': reverse('competitions:sports_create'),
    }
    if request.POST:
        if form.is_valid():
            cats_m2m = form.cleaned_data['categories']
            form_reg = form.save(commit=True)
            form_reg.categories.set(cats_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Esporte adicionado com sucesso.')
            return redirect(reverse('competitions:sports'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'competitions/pages/sport-create.html', context)


def tests(request):
    TeamFactory()
    # TestFactory.create_batch(size=1)  # Remove if needed
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


@login_required
@admin_required
def tests_create(request):
    form = TestForm(request.POST or None, request.FILES or None)
    context = {
        'title': 'Criar prova',
        'form': form,
        'form_action': reverse('competitions:tests_create'),
    }
    if request.POST:
        if form.is_valid():
            teams_m2m = form.cleaned_data['teams']
            form_reg = form.save(commit=True)
            form_reg.teams.set(teams_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Teste adicionado com sucesso.')
            return redirect(reverse('competitions:tests'))
    # else:
    # messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'competitions/pages/test-create.html', context)

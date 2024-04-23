from random import choices

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from competitions.models import Sport, Test, TestTeam
from competitions.tests.factories import CategoryFactory, SportFactory, TestFactory
from editions.models import Team
from editions.tests.factories import TeamFactory
from helpers.decorators import admin_required

from .forms import SportForm, TestForm, TestTeamForm


def competitions(request):
    return redirect(reverse('competitions:sports'))


def sports(request):
    # cats = CategoryFactory.create_batch(size=3)  # Remove if needed
    # SportFactory.create_batch(size=1, categories=choices(cats))  # Remove if needed
    CategoryFactory.create_batch(size=3)  # Remove if needed
    context = {
        'title': 'Competições',
        'page_variant': 'sports',
        'db_regs': Sport.objects.all(),
        'search_url': reverse('competitions:sports_search'),
    }
    return render(request, 'competitions/pages/sports.html', context)


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
    form = SportForm(request.POST or None, request.FILES or None)
    context = {
        'title': 'Adicionar esporte',
        'form': form,
        'form_action': reverse('competitions:sports_create'),
    }
    if request.POST:
        if form.is_valid():
            cats_m2m = form.cleaned_data['categories']
            form_reg = form.save(commit=True)
            form_reg.categories.add(*cats_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Esporte adicionado com sucesso.')
            return redirect(reverse('competitions:sports'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'competitions/pages/sport-create.html', context)


@login_required
@admin_required
def sports_edit(request, slug): ...


def tests(request):
    TeamFactory()
    # TestFactory.create_batch(size=1)  # Remove if needed
    context = {
        'title': 'Competições',
        'page_variant': 'tests',
        'db_regs': Test.objects.all(),
        'search_url': reverse('competitions:tests_search'),
    }
    return render(request, 'competitions/pages/tests.html', context)


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
        'title': 'Adicionar prova',
        'form': form,
        'form_action': reverse('competitions:tests_create'),
    }
    if request.POST:
        if form.is_valid():
            teams_m2m = form.cleaned_data['teams']
            form_reg = form.save(commit=True)
            form_reg.teams.add(*teams_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Prova adicionada com sucesso.')
            return redirect(reverse('competitions:tests'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'competitions/pages/test-create.html', context)


@login_required
@admin_required
def tests_edit(request, slug):
    test_obj = get_object_or_404(Test, slug=slug)
    form = TestForm(request.POST or None, request.FILES or None, instance=test_obj)
    form.fields['teams'].required = False
    TestTeamFormSet = modelformset_factory(
        TestTeam,
        TestTeamForm,
        extra=0,
        fields=['score', 'classification'],
    )
    form_teams = TestTeamFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=TestTeam.objects.filter(test__pk=test_obj.pk),
    )
    if request.POST:
        if form.is_valid() and form_teams.is_valid():
            form.save()
            form_teams.save()
            messages.success(request, 'Prova editada com sucesso.')
            return redirect(reverse('competitions:tests'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Editar prova',
        'test': test_obj,
        'form': form,
        'form_teams': form_teams,
        'form_action': reverse(
            'competitions:tests_edit', kwargs={'slug': test_obj.slug}
        ),
    }
    return render(request, 'competitions/pages/test-edit.html', context)

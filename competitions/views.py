from random import choices

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse

from competitions.models import Match, MatchTeam, Sport, SportCategory, Test, TestTeam
from competitions.tests.factories import CategoryFactory, SportFactory, TestFactory
from editions.models import Edition, Team
from editions.tests.factories import TeamFactory
from helpers.decorators import admin_required

from .forms import MatchForm, MatchTeamForm, SportForm, TestForm, TestTeamForm


def competitions(request):
    return redirect(reverse('competitions:sports'))


def sports(request):
    # cats = CategoryFactory.create_batch(size=3)  # Remove if needed
    # SportFactory.create_batch(size=1, categories=choices(cats))  # Remove if needed
    # CategoryFactory.create_batch(size=3)  # Remove if needed
    cat1 = CategoryFactory(name='Masculino')
    cat2 = CategoryFactory(name='Feminino')
    cat3 = CategoryFactory(name='Misto')
    sport1 = SportFactory(name='Futsal', categories=(cat1, cat2))
    sport2 = SportFactory(name='Vôlei', categories=(cat1, cat3))
    context = {
        'title': 'Competições',
        'page_variant': 'sports',
        'db_regs': Sport.objects.order_by('name'),
        'search_url': reverse('competitions:sports_search'),
    }
    return render(request, 'competitions/pages/sports.html', context)


def sports_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
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
        'title': 'Criar esporte',
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
def sports_edit(request, slug):
    obj = get_object_or_404(Sport, slug=slug)
    form = SportForm(request.POST or None, request.FILES or None, instance=obj)
    form.fields['name'].disabled = True
    context = {
        'title': 'Editar esporte',
        'form': form,
        'form_action': reverse('competitions:sports_edit', kwargs={'slug': obj.slug}),
    }
    if request.POST:
        if form.is_valid():
            cats_m2m = form.cleaned_data['categories']
            form_reg = form.save(commit=True)
            form_reg.categories.add(*cats_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Esporte editado com sucesso.')
            return redirect(reverse('competitions:sports'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'competitions/pages/sport-create.html', context)


def sports_detailed(request, slug):
    # test = get_list_or_404(SportCategory, sport__slug=slug)
    # obj = get_list_or_404(Match, sport_category__sport__slug=slug)
    obj = Match.objects.get(sport_category__sport__slug=slug)
    context = {
        'title': f'Esportes - {obj[0].sport.name}',
        'sport_name': obj[0].sport.name,
        'regs': obj,
    }
    return render(request, 'competitions/pages/sport-detailed.html', context)


@login_required
@admin_required
def matches_create(request, pk):
    edition_obj = get_object_or_404(Edition, pk=pk)
    form = MatchForm(
        request.POST or None,
        request.FILES or None,
        edition_obj=edition_obj,
    )
    context = {
        'title': 'Criar partida',
        'form': form,
    }
    if request.POST:
        if form.is_valid():
            form_reg = form.save(commit=False)
            form_reg.edition = edition_obj
            form_reg.save()
            form.save_m2m()
            messages.success(request, 'Partida adicionada com sucesso.')
            return redirect(reverse('editions:editions_detailed', kwargs={'pk': pk}))
    return render(request, 'competitions/pages/match-create.html', context)


@login_required
@admin_required
def matches_edit(request, pk):
    match_obj = get_object_or_404(Match, pk=pk)
    form = MatchForm(request.POST or None, request.FILES or None, instance=match_obj)
    form.fields['sport_category'].disabled = True
    form.fields['teams'].disabled = True
    MatchTeamFormSet = modelformset_factory(
        MatchTeam,
        MatchTeamForm,
        extra=0,
        fields=['score'],
    )
    form_matches = MatchTeamFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=MatchTeam.objects.filter(match__pk=match_obj.pk),
    )
    if request.POST:
        if form.is_valid() and form_matches.is_valid():
            form.save()
            form_matches.save()
            messages.success(request, 'Partida editada com sucesso.')
            return redirect(reverse('editions:editions'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')

    context = {
        'title': 'Editar partida',
        'form': form,
        'form_matches': form_matches,
        'form_action': reverse(
            'competitions:matches_edit', kwargs={'pk': match_obj.pk}
        ),
    }
    return render(request, 'competitions/pages/match-edit.html', context)


def tests(request):
    TeamFactory()
    # TestFactory.create_batch(size=1)  # Remove if needed
    context = {
        'title': 'Competições',
        'page_variant': 'tests',
        'db_regs': Test.objects.order_by('-date_time'),
        'search_url': reverse('competitions:tests_search'),
    }
    return render(request, 'competitions/pages/tests.html', context)


def tests_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
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
        fields=['score'],
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

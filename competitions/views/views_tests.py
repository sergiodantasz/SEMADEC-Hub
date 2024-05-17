from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from competitions.forms import (
    TestForm,
    TestTeamForm,
)
from competitions.models import Test, TestTeam
from helpers.decorators import admin_required
from teams.models import Team


def tests(request):
    context = {
        'title': 'Competições',
        'page_variant': 'tests',
        'db_regs': Test.objects.order_by('-date_time'),
        'search_url': reverse('competitions:tests:search'),
    }
    return render(request, 'competitions/pages/tests.html', context)


def tests_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
        return redirect(reverse('competitions:tests:home'))

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
    if not Team.objects.exists():
        messages.error(request, 'Adicione ao menos um time antes de criar uma prova.')
        return redirect(reverse('competitions:tests:home'))
    context = {
        'title': 'Criar prova',
        'form': form,
    }
    if request.POST:
        if form.is_valid():
            teams_m2m = form.cleaned_data['teams']
            form_reg = form.save(commit=True)
            form_reg.teams.add(*teams_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Prova adicionada com sucesso.')
            return redirect(reverse('competitions:tests:home'))
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
            return redirect(reverse('competitions:tests:home'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Editar prova',
        'test': test_obj,
        'form': form,
        'form_teams': form_teams,
    }
    return render(request, 'competitions/pages/test-edit.html', context)


def tests_detailed(request, slug):
    test = get_object_or_404(Test, slug=slug)

    context = {
        'title': test.title,
        'test': test,
    }
    return render(request, 'competitions/pages/test-detailed.html', context)


def tests_delete(request, slug): ...

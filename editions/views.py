from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import HiddenInput, inlineformset_factory, modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from editions.models import Edition, EditionTeam, Team
from editions.tests.factories import (
    EditionWith2TeamsFactory,
    TeamFactory,
)
from helpers.decorators import admin_required
from helpers.model import is_owner

from .forms import EditionForm, EditionTeamForm, TeamForm


def editions(request):
    # EditionWith2TeamsFactory.create_batch(3)  # Remove if needed
    TeamFactory.create_batch(5)  # Remove if needed
    context = {
        'title': 'Edições',
        'db_regs': Edition.objects.order_by('-year'),
    }
    return render(request, 'editions/pages/editions.html', context)


@login_required
@admin_required
def editions_create(request):
    form = EditionForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            teams_m2m = form.cleaned_data['teams']
            form_reg = form.save(commit=True)
            form_reg.teams.add(*teams_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(request, 'Edição adicionada com sucesso.')
            return redirect(reverse('editions:editions'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Adicionar edição',
        'form': form,
        'form_action': reverse('editions:editions_create'),
    }
    return render(request, 'editions/pages/edition-create.html', context)


@login_required
@admin_required
def editions_edit(request, year):
    edition_obj = get_object_or_404(Edition, year=year)
    form = EditionForm(
        request.POST or None, request.FILES or None, instance=edition_obj
    )
    form.fields['year'].disabled = True
    form.fields['teams'].required = False
    EditionTeamFormSet = modelformset_factory(
        EditionTeam,
        EditionTeamForm,
        extra=0,
        fields=['score', 'classification'],  # add 'team' if desired
    )
    form_teams = EditionTeamFormSet(
        request.POST or None,
        request.FILES or None,
        queryset=EditionTeam.objects.filter(edition__year=edition_obj.year),
    )

    if request.POST:
        if form.is_valid() and form_teams.is_valid():
            form.save()
            form_teams.save()
            messages.success(request, 'Edição editada com sucesso.')
            return redirect(reverse('editions:editions'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Editar edição',
        'edition': edition_obj,
        'form': form,
        'form_teams': form_teams,
        'form_action': reverse(
            'editions:editions_edit', kwargs={'year': edition_obj.year}
        ),
    }
    return render(request, 'editions/pages/edition-edit.html', context)


@login_required
@admin_required
def editions_delete(request, year):
    try:
        edition_obj = get_object_or_404(Edition, year=year)
        edition_obj.delete()
    except Exception:
        messages.error(request, 'Não foi possível remover esta edição.')
    else:
        messages.success(request, 'Edição removida com sucesso!')
    return redirect(reverse('editions:editions'))

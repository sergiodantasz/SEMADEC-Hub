from random import choices

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from competitions.forms import (
    MatchForm,
    MatchTeamForm,
)
from competitions.models import Match, MatchTeam
from editions.models import Edition
from helpers.decorators import admin_required


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
    }
    return render(request, 'competitions/pages/match-edit.html', context)

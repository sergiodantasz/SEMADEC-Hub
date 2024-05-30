from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.teams.forms import TeamForm
from apps.teams.models import Class, Team
from helpers.decorators import admin_required


def teams(request):
    context = {
        'title': 'Times',
        'db_regs': Team.objects.order_by('name'),
        'search_url': reverse('teams:search'),
    }
    return render(request, 'teams/pages/teams.html', context)


@login_required
@admin_required
def teams_create(request):
    form = TeamForm(request.POST or None, request.FILES or None)
    if not Class.objects.exists():
        messages.error(
            request, 'Adicione ao menos uma turma antes de criar uma edição.'
        )
        return redirect(reverse('teams:home'))
    if request.POST:
        if form.is_valid():
            reg = form.save(commit=False)
            reg.save()
            form.save_m2m()
            messages.success(request, 'Time adicionado com sucesso.')
            return redirect(reverse('teams:home'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Criar time',
        'form': form,
        'form_action': reverse('teams:create'),
    }
    return render(request, 'teams/pages/team-create.html', context)


def teams_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
        return redirect(reverse('teams:home'))

    db_regs = Team.objects.filter(
        name__icontains=querystr,
        # Add classes search
    ).order_by('name')
    context = {
        'title': 'Times',
        'db_regs': db_regs,
    }
    return render(request, 'teams/pages/teams.html', context)


@login_required
@admin_required
def teams_edit(request, slug):
    obj = get_object_or_404(Team, slug=slug)
    form = TeamForm(request.POST or None, request.FILES or None, instance=obj)
    if request.POST:
        if form.is_valid():
            reg = form.save(commit=True)
            reg.save()
            messages.success(request, 'Time editado com sucesso.')
            return redirect(reverse('teams:home'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Editar time',
        'form': form,
        'form_action': reverse('teams:edit', kwargs={'slug': obj.slug}),
    }
    return render(request, 'teams/pages/team-create.html', context)


@login_required
@admin_required
def teams_delete(request, slug):
    try:
        reg = get_object_or_404(Team, slug=slug)
        reg.delete()
    except DatabaseError:
        messages.error(request, 'Não foi possível remover este time.')
    else:
        messages.success(request, 'Time removido com sucesso!')
    return redirect(reverse('teams:home'))

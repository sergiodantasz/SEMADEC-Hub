from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from helpers.decorators import admin_required
from teams.forms import ClassForm
from teams.models import Class, Course


def classes(request):
    context = {
        'title': 'Turmas',
        'db_regs': Class.objects.order_by('name'),
        'search_url': reverse('teams:classes:search'),
    }
    return render(request, 'teams/pages/classes.html', context)


@login_required
@admin_required
def classes_create(request):
    form = ClassForm(request.POST or None, request.FILES or None)
    if not Course.objects.exists():
        messages.error(request, 'Adicione ao menos um curso antes de criar uma turma.')
        return redirect(reverse('teams:classes:home'))
    if request.POST:
        if form.is_valid():
            reg = form.save(commit=True)
            messages.success(request, 'Turma adicionada com sucesso.')
            return redirect(reverse('teams:classes:home'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Criar turma',
        'form': form,
        'form_action': reverse('teams:classes:create'),
    }
    return render(request, 'teams/pages/class-create.html', context)


def classes_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
        return redirect(reverse('teams:classes:home'))

    db_regs = Class.objects.filter(
        Q(
            Q(name__icontains=querystr) | Q(course__name__icontains=querystr),
        )
    ).order_by('name')
    context = {
        'title': 'Turmas',
        'db_regs': db_regs,
    }
    return render(request, 'teams/pages/classes.html', context)


@login_required
@admin_required
def classes_edit(request, slug):
    obj = get_object_or_404(Class, slug=slug)
    form = ClassForm(request.POST or None, request.FILES or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Turma editada com sucesso.')
            return redirect(reverse('teams:classes:home'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Editar turma',
        'form': form,
        'form_action': reverse('teams:classes:edit', kwargs={'slug': obj.slug}),
    }
    return render(request, 'teams/pages/class-create.html', context)


@login_required
@admin_required
def classes_delete(request, slug):
    try:
        reg = get_object_or_404(Class, slug=slug)
        reg.delete()
    except DatabaseError:
        messages.error(request, 'Não foi possível remover esta turma.')
    else:
        messages.success(request, 'Turma removida com sucesso!')
    return redirect(reverse('teams:classes:home'))

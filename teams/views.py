from random import choices

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse

from competitions.models import Match, MatchTeam, Sport, SportCategory, Test, TestTeam
from competitions.tests.factories import CategoryFactory, SportFactory, TestFactory
from editions.models import Edition
from editions.tests.factories import TeamFactory
from helpers.decorators import admin_required
from teams.forms import ClassForm, CourseForm, TeamForm
from teams.models import Class, Course, Team


# Teams
def teams(request):
    context = {
        'title': 'Times',
        'db_regs': Team.objects.order_by('name'),
        'search_url': reverse('teams:teams_search'),
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
        return redirect(reverse('teams:teams'))
    if request.POST:
        if form.is_valid():
            reg = form.save(commit=False)
            reg.save()
            form.save_m2m()
            messages.success(request, 'Time adicionado com sucesso.')
            return redirect(reverse('teams:teams'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Criar time',
        'form': form,
        'form_action': reverse('teams:teams_create'),
    }
    return render(request, 'teams/pages/team-create.html', context)


def teams_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
        return redirect(reverse('teams:teams'))

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
def teams_edit(request, slug): ...


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
    return redirect(reverse('teams:teams'))


# Classes
def classes(request):
    context = {
        'title': 'Turmas',
        'db_regs': Class.objects.order_by('name'),
        'search_url': reverse('teams:classes_search'),
    }
    return render(request, 'teams/pages/classes.html', context)


@login_required
@admin_required
def classes_create(request):
    form = ClassForm(request.POST or None, request.FILES or None)
    if not Course.objects.exists():
        messages.error(request, 'Adicione ao menos um curso antes de criar uma turma.')
        return redirect(reverse('teams:classes'))
    if request.POST:
        if form.is_valid():
            reg = form.save(commit=True)
            messages.success(request, 'Turma adicionada com sucesso.')
            return redirect(reverse('teams:classes'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Criar turma',
        'form': form,
        'form_action': reverse('teams:classes_create'),
    }
    return render(request, 'teams/pages/class-create.html', context)


def classes_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
        return redirect(reverse('teams:classes'))

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
def classes_edit(request, slug): ...


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
    return redirect(reverse('teams:classes'))


# Courses
def courses(request):
    context = {
        'title': 'Cursos',
        'db_regs': Course.objects.order_by('name'),
        'search_url': reverse('teams:courses_search'),
    }
    return render(request, 'teams/pages/courses.html', context)


@login_required
@admin_required
def courses_create(request):
    form = CourseForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            reg = form.save(commit=True)
            messages.success(request, 'Curso adicionado com sucesso.')
            return redirect(reverse('teams:courses'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Criar curso',
        'form': form,
        'form_action': reverse('teams:courses_create'),
    }
    return render(request, 'teams/pages/course-create.html', context)


def courses_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
        return redirect(reverse('teams:courses'))

    db_regs = Course.objects.filter(
        name__icontains=querystr,
    ).order_by('name')
    context = {
        'title': 'Cursos',
        'db_regs': db_regs,
    }
    return render(request, 'teams/pages/courses.html', context)


@login_required
@admin_required
def courses_edit(request, slug): ...


@login_required
@admin_required
def courses_delete(request, slug):
    try:
        reg = get_object_or_404(Course, slug=slug)
        reg.delete()
    except DatabaseError:
        messages.error(request, 'Não foi possível remover este curso.')
    else:
        messages.success(request, 'Curso removido com sucesso!')
    return redirect(reverse('teams:courses'))

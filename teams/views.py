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
from editions.models import Class, Course, Edition, Team
from editions.tests.factories import TeamFactory
from helpers.decorators import admin_required
from teams.forms import ClassForm, CourseForm, TeamForm


# Teams
def teams(request): ...


@login_required
@admin_required
def teams_create(request):
    form = TeamForm(request.POST or None, request.FILES or None)
    if not Class.objects.exists():
        messages.error(
            request, 'Adicione ao menos uma turma antes de criar uma edição.'
        )
        return redirect(reverse('home:home'))  # Change later
    if request.POST:
        if form.is_valid():
            reg = form.save(commit=False)
            reg.save()
            form.save_m2m()
            messages.success(request, 'Time adicionado com sucesso.')
            return redirect(reverse('home:home'))  # Change later
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Criar time',
        'form': form,
        'form_action': reverse('teams:teams_create'),
    }
    return render(request, 'teams/pages/team-create.html', context)


def teams_search(request): ...


@login_required
@admin_required
def teams_edit(request, slug): ...


@login_required
@admin_required
def teams_delete(request, slug): ...


# Classes
def classes(request): ...


@login_required
@admin_required
def classes_create(request):
    form = ClassForm(request.POST or None, request.FILES or None)
    if not Course.objects.exists():
        messages.error(request, 'Adicione ao menos um curso antes de criar uma turma.')
        return redirect(reverse('home:home'))  # Change later
    if request.POST:
        if form.is_valid():
            reg = form.save(commit=True)
            messages.success(request, 'Turma adicionada com sucesso.')
            return redirect(reverse('home:home'))  # Change later
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Criar turma',
        'form': form,
        'form_action': reverse('teams:classes_create'),
    }
    return render(request, 'teams/pages/class-create.html', context)


def classes_search(request): ...


@login_required
@admin_required
def classes_edit(request, slug): ...


@login_required
@admin_required
def classes_delete(request, slug): ...


# Courses
def courses(request): ...


@login_required
@admin_required
def courses_create(request):
    form = CourseForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            reg = form.save(commit=True)
            messages.success(request, 'Curso adicionado com sucesso.')
            return redirect(reverse('home:home'))  # Change later
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Criar curso',
        'form': form,
        'form_action': reverse('teams:courses_create'),
    }
    return render(request, 'teams/pages/course-create.html', context)


def courses_search(request): ...


@login_required
@admin_required
def courses_edit(request, slug): ...


@login_required
@admin_required
def courses_delete(request, slug): ...

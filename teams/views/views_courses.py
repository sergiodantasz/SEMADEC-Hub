from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from helpers.decorators import admin_required
from teams.forms import CourseForm
from teams.models import Course


def courses(request):
    context = {
        'title': 'Cursos',
        'db_regs': Course.objects.order_by('name'),
        'search_url': reverse('teams:courses:search'),
    }
    return render(request, 'teams/pages/courses.html', context)


@login_required
@admin_required
def courses_create(request):
    form = CourseForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Curso adicionado com sucesso.')
            return redirect(reverse('teams:courses:home'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Criar curso',
        'form': form,
        'form_action': reverse('teams:courses:create'),
    }
    return render(request, 'teams/pages/course-create.html', context)


def courses_search(request):
    querystr = request.GET.get('q').strip()

    if not querystr:
        messages.warning(request, 'Digite um termo de busca válido.')
        return redirect(reverse('teams:courses:home'))

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
def courses_edit(request, slug):
    obj = get_object_or_404(Course, slug=slug)
    form = CourseForm(request.POST or None, request.FILES or None, instance=obj)
    if request.POST:
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Curso editado com sucesso.')
            return redirect(reverse('teams:courses:home'))
        messages.error(request, 'Preencha os campos do formulário corretamente.')
    context = {
        'title': 'Editar curso',
        'form': form,
        'form_action': reverse('teams:courses:edit', kwargs={'slug': obj.slug}),
    }
    return render(request, 'teams/pages/course-create.html', context)


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
    return redirect(reverse('teams:courses:home'))

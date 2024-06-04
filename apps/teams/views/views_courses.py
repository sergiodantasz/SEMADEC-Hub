from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.forms import modelformset_factory
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView

from apps.home.views.views import MessageMixin
from apps.teams.forms import CourseForm
from apps.teams.models import Course
from helpers.decorators import admin_required


class CourseView(ListView):
    model = Course
    template_name = 'teams/pages/courses.html'
    context_object_name = 'db_regs'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Course.objects.order_by('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Cursos', 'search_url': reverse('teams:courses:search')}
        return context


class CourseSearchView(ListView):
    model = Course
    template_name = 'teams/pages/courses.html'
    context_object_name = 'db_regs'
    paginate_by = 10
    warning_message = 'Digite um termo de busca válido.'

    def get_search_term(self) -> str:
        return self.request.GET.get('q', '').strip()

    def get_queryset(self) -> QuerySet[Any]:
        querystr = self.get_search_term()
        if not querystr:
            messages.warning(self.request, self.warning_message)
        queryset = Course.objects.filter(
            name__icontains=querystr,
        ).order_by('name')
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Cursos'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class CourseCreateView(MessageMixin, FormView):
    template_name = 'teams/pages/course-create.html'
    form_class = CourseForm
    success_url = reverse_lazy('teams:courses:home')
    success_message = 'Curso adicionado com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar curso'}
        return context

    def form_valid(self, form):
        form_reg = form.save()
        return super().form_valid(form)


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


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class CourseEditView(MessageMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'teams/pages/course-create.html'
    success_url = reverse_lazy('teams:courses:home')
    success_message = 'Curso editado com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context |= {'title': 'Editar curso'}
        return context

    def form_valid(self, form):
        form_reg = form.save()
        return super().form_valid(form)


class CourseDeleteView(MessageMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('teams:courses:home')
    success_message = 'Curso removido com sucesso!'
    # error_message = 'Não foi possível remover este curso.'

    def get(self, request, *args, **kwargs):
        self.delete(request, *args, **kwargs)
        return redirect(self.success_url)

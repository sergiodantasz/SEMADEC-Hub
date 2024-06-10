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
from home.views import BaseCreateView, BaseListView, BaseSearchView

from apps.home.views.views import MessageMixin
from apps.teams.forms import CourseForm
from apps.teams.models import Course
from helpers.decorators import admin_required


class CourseListView(BaseListView):
    model = Course
    template_name = 'teams/pages/courses.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Cursos',
        }
        return context


class CourseSearchView(BaseSearchView):
    model = Course
    template_name = 'teams/pages/courses.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(name__icontains=self.querystr)
        return super().get_queryset(query, 'name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Cursos'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class CourseCreateView(BaseCreateView):
    template_name = 'teams/pages/course-create.html'
    form_class = CourseForm
    success_url = reverse_lazy('teams:courses:home')
    msg = {
        'success': {'form': 'Curso adicionado com sucesso.'},
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar curso'}
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


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

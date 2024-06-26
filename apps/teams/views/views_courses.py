from typing import Any

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.decorators import method_decorator

from apps.teams.forms import CourseForm
from apps.teams.models import Course
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseEditView,
    BaseListView,
    BaseSearchView,
)
from helpers.decorators import admin_required


class CourseListView(BaseListView):
    model = Course
    template_name = 'teams/pages/courses.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = {'title': 'Cursos'}
        return super().get_context_data(**context)


class CourseSearchView(BaseSearchView):
    model = Course
    template_name = 'teams/pages/courses.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(name__icontains=self.querystr)
        return super().get_queryset(query, 'name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = {'title': 'Cursos'}
        return super().get_context_data(**context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class CourseCreateView(BaseCreateView):
    form_class = CourseForm
    template_name = 'teams/pages/course-create.html'
    msg = {
        'success': {'form': 'Curso adicionado com sucesso.'},
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_context_data(self, **kwargs):
        context = {'title': 'Criar curso'}
        return super().get_context_data(**context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class CourseEditView(BaseEditView):
    form_class = CourseForm
    template_name = 'teams/pages/course-create.html'
    msg = {
        'success': {'form': 'Curso editado com sucesso.'},
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_context_data(self, **kwargs):
        context = {'title': 'Editar curso'}
        return super().get_context_data(**context)


class CourseDeleteView(BaseDeleteView):
    model = Course
    msg = {
        'success': {'form': 'Curso removido com sucesso!'},
        'error': {'form': 'Não foi possível remover este curso.'},
    }

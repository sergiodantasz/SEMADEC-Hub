from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from apps.home.views.views import BaseCreateView, BaseDeleteView, BaseEditView
from apps.teams.forms import ClassForm
from apps.teams.models import Class, Course
from base.views import BaseListView, BaseSearchView
from helpers.decorators import admin_required


class ClassListView(BaseListView):
    model = Class
    template_name = 'teams/pages/classes.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Turmas',
        }
        return context


class ClassSearchView(BaseSearchView):
    model = Class
    template_name = 'teams/pages/classes.html'

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(
            Q(name__icontains=self.querystr) | Q(course__name__icontains=self.querystr),
        )
        return super().get_queryset(query, 'name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Turmas'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ClassCreateView(BaseCreateView):
    form_class = ClassForm
    template_name = 'teams/pages/class-create.html'
    msg = {
        'success': {'form': 'Turma adicionada com sucesso.'},
        'error': {
            'form': 'Preencha os campos do formulário corretamente.',
            'course': 'Adicione ao menos um curso antes de criar uma turma.',
        },
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar turma'}
        return context

    def get(self, request, *args, **kwargs):
        if not self.is_model_populated(Course):
            messages.error(self.request, self.msg['error']['course'])
            return redirect(self.get_success_url())
        context = self.get_context_data()
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ClassEditView(BaseEditView):
    model = Class
    form_class = ClassForm
    template_name = 'teams/pages/class-create.html'
    msg = {
        'success': {'form': 'Turma editada com sucesso.'},
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Editar turma'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ClassDeleteView(BaseDeleteView):
    model = Class
    msg = {
        'success': {'form': 'Turma removida com sucesso!'},
        'error': {'form': 'Não foi possível remover esta turma.'},
    }

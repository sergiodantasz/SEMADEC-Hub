from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from home.views import BaseListView, BaseSearchView, MessageMixin

from apps.home.views.views import BaseCreateView
from apps.teams.forms import TeamForm
from apps.teams.models import Class, Team
from helpers.decorators import admin_required


class TeamListView(BaseListView):
    model = Team
    template_name = 'teams/pages/teams.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Times',
        }
        return context


class TeamSearchView(BaseSearchView):
    model = Team
    template_name = 'teams/pages/teams.html'

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(name__icontains=self.querystr)
        # Add query for teams m2m
        return super().get_queryset(query, 'name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Times'}
        return context


class TeamCreateView(BaseCreateView):
    form_class = TeamForm
    template_name = 'teams/pages/team-create.html'
    msg = {
        'success': {'form': 'Time adicionado com sucesso.'},
        'error': {
            'form': 'Preencha os campos do formulário corretamente.',
            'class': 'Adicione ao menos uma turma antes de criar uma edição.',
        },
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar time'}
        return context

    def get(self, request, *args, **kwargs):
        if not self.is_model_populated(Class):
            messages.error(self.request, self.msg['error']['class'])
            return redirect(self.get_success_url())
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TeamEditView(MessageMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/pages/team-create.html'
    success_url = reverse_lazy('teams:home')
    success_message = 'Time editado com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Editar time'}
        return context

    def form_valid(self, form):
        form_reg = form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TeamDeleteView(MessageMixin, DeleteView):
    model = Team
    success_url = reverse_lazy('teams:home')
    success_message = 'Time removido com sucesso!'

    def get(self, request, *args, **kwargs):
        self.delete(request, *args, **kwargs)
        return redirect(self.success_url)

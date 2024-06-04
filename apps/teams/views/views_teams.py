from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from home.views import MessageMixin

from apps.teams.forms import TeamForm
from apps.teams.models import Class, Team
from helpers.decorators import admin_required


class TeamView(ListView):
    model = Team
    template_name = 'teams/pages/teams.html'
    context_object_name = 'db_regs'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Team.objects.order_by('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Times',
            'search_url': reverse('teams:search'),
        }
        return context


class TeamSearchView(MessageMixin, ListView):
    model = Team
    template_name = 'teams/pages/teams.html'
    context_object_name = 'db_regs'
    warning_message = 'Digite um termo de busca válido.'

    def get_search_term(self) -> str:
        return self.request.GET.get('q', '').strip()

    def get_queryset(self) -> QuerySet[Any]:
        querystr = self.get_search_term()
        # Test with MessageMixin
        if not querystr:
            messages.warning(self.request, self.warning_message)
        queryset = Team.objects.filter(
            name__icontains=querystr,
            # Add classes search
        ).order_by('name')
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Times'}
        return context


class TeamCreateView(MessageMixin, FormView):
    form_class = TeamForm
    template_name = 'teams/pages/team-create.html'
    success_url = reverse_lazy('teams:home')
    success_message = 'Time adicionado com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'
    error_message_class = 'Adicione ao menos uma turma antes de criar uma edição.'

    def is_model_populated(self, model: Model):
        return model.objects.exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar time'}
        return context

    def get(self, request, *args, **kwargs):
        if not self.is_model_populated(Class):
            messages.error(self.request, self.error_message_class)
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        form_reg = form.save()
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

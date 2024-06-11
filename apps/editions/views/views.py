from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import HiddenInput, modelformset_factory
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from home.views import BaseListView, BaseSearchView

from apps.competitions.models import Sport
from apps.editions.forms import EditionForm, EditionTeamForm
from apps.editions.models import Edition, EditionTeam
from apps.home.views.views import BaseCreateView, BaseDeleteView, BaseEditView
from apps.teams.models import Team
from helpers.decorators import admin_required


class EditionListView(BaseListView):
    model = Edition
    template_name = 'editions/pages/editions.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('-year')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Edições'}
        return context


class EditionDetailView(DetailView):
    model = Edition
    template_name = 'editions/pages/edition-detailed.html'
    context_object_name = 'reg'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context |= {'matches': self.object.matches.all()}
        return context


class EditionSearchView(BaseSearchView):
    model = Edition
    template_name = 'editions/pages/editions.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(
            Q(year__icontains=self.querystr)
            | Q(name__icontains=self.querystr)
            | Q(edition_type__icontains=self.querystr)
            | Q(theme__icontains=self.querystr)
        )
        return super().get_queryset(query, '-year')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Edições'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EditionCreateView(BaseCreateView):
    form_class = EditionForm
    template_name = 'editions/pages/edition-create.html'
    msg = {
        'success': {'form': 'Edição adicionada com sucesso.'},
        'error': {
            'form': 'Preencha os campos do formulário corretamente.',
            'sport': 'Adicione ao menos um esporte antes de criar uma edição.',
            'team': 'Adicione ao menos um time antes de criar uma edição.',
        },
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar edição'}
        return context

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if not self.is_model_populated(Sport):
            messages.error(self.request, self.msg['error']['sport'])
            return redirect(self.get_success_url())
        if not self.is_model_populated(Team):
            messages.error(self.request, self.msg['error']['team'])
            return redirect(self.get_success_url())
        context = self.get_context_data()
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EditionEditView(BaseEditView):
    model = Edition
    form_class = EditionForm
    form_teams = modelformset_factory(
        EditionTeam,
        EditionTeamForm,
        extra=0,
        fields=['score'],
    )
    template_name = 'editions/pages/edition-edit.html'
    msg = {
        'success': {'form': 'Edição editada com sucesso.'},
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Editar edição',
            'form_teams': self.get_form_teams(),
        }
        return context

    def get_form(self, form_class=None):
        form = self.form_class(self.request.POST or None, instance=self.get_object())
        form.fields['year'].disabled = True
        form.fields['sports'].disabled = True
        form.fields['teams'].required = False
        form.fields['teams'].widget = HiddenInput()
        form.fields['sports'].required = False
        return form

    def get_form_teams(self, form_class=None):
        form_teams = self.form_teams(
            self.request.POST or None,
            queryset=EditionTeam.objects.filter(
                edition__pk=self.get_object().pk,
            ),
        )
        return form_teams

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        form = self.get_form()
        form_teams = self.get_form_teams()
        if form.is_valid() and form_teams.is_valid():
            form.save()
            form_teams.save()
            messages.success(self.request, self.msg['success']['form'])
        else:
            messages.error(request, self.msg['error']['form'])
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EditionDeleteView(BaseDeleteView):
    model = Edition
    msg = {
        'success': {'form': 'Edição removida com sucesso!'},
        'error': {'form': 'Não foi possível remover esta edição.'},
    }

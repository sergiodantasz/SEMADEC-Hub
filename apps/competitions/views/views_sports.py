from typing import Any

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView

from apps.competitions.forms import (
    SportForm,
)
from apps.competitions.models import Sport
from apps.competitions.tests.factories import CategoryFactory
from apps.editions.models import Edition
from apps.home.views.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseEditView,
)
from base.views import BaseListView, BaseSearchView
from helpers.decorators import admin_required


class SportListView(BaseListView):
    model = Sport
    template_name = 'competitions/pages/competitions.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        # Remove later
        cat_masculino = CategoryFactory(name='Masculino')
        cat_feminino = CategoryFactory(name='Feminino')
        cat_misto = CategoryFactory(name='Misto')
        # Remove later
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Competições',
            'page_variant': 'sports',
        }
        return context


class SportSearchView(BaseSearchView):
    model = Sport
    template_name = 'competitions/pages/competitions.html'
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(name__icontains=self.querystr)
        return super().get_queryset(query, 'name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Competições', 'page_variant': 'sports'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class SportCreateView(BaseCreateView):
    form_class = SportForm
    template_name = 'competitions/pages/sport-create.html'
    # Add error for non existing categories
    msg = {
        'success': {'form': 'Esporte adicionado com sucesso.'},
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar esporte'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class SportEditView(BaseEditView):
    model = Sport
    form_class = SportForm
    template_name = 'competitions/pages/sport-create.html'
    msg = {
        'success': {'form': 'Esporte editado com sucesso.'},
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Editar esporte'}
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].disabled = True
        return form


class SportDetailView(BaseDetailView):
    model = Sport
    template_name = 'competitions/pages/sport-detailed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        editions = Edition.objects.filter(
            matches__sport_category__sport=self.object
        ).distinct()
        editions_matches = dict()
        for edition in editions:
            query_matches = edition.get_matches.filter(
                sport_category__sport=self.object
            )
            editions_matches.update({edition: query_matches})
        context |= {'title': self.object.name, 'regs': editions_matches}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class SportDeleteView(BaseDeleteView):
    model = Sport
    msg = {
        'success': {'form': 'Esporte removido com sucesso!'},
        'error': {'form': 'Não foi possível remover este esporte.'},
    }

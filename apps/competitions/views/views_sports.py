from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from home.views import MessageMixin

from apps.competitions.forms import (
    SportForm,
)
from apps.competitions.models import Sport
from apps.competitions.tests.factories import CategoryFactory
from apps.editions.models import Edition
from helpers.decorators import admin_required


class SportListView(ListView):
    model = Sport
    template_name = 'competitions/pages/competitions.html'
    context_object_name = 'db_regs'
    paginate_by = 10

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
            'search_url': reverse('competitions:sports:search'),
        }
        return context


class SportSearchView(ListView):
    model = Sport
    template_name = 'competitions/pages/competitions.html'
    context_object_name = 'db_regs'
    # paginate_by = 10
    warning_message = 'Digite um termo de busca válido.'

    def get_search_term(self) -> str:
        return self.request.GET.get('q', '').strip()

    def get_queryset(self) -> QuerySet[Any]:
        querystr = self.get_search_term()
        if not querystr:
            messages.warning(self.request, self.warning_message)
        queryset = Sport.objects.filter(name__icontains=querystr).order_by('name')
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Competições', 'page_variant': 'sports'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class SportCreateView(MessageMixin, FormView):
    template_name = 'competitions/pages/sport-create.html'
    form_class = SportForm
    # Add error for non existing categories
    success_url = reverse_lazy('competitions:sports:home')
    success_message = 'Esporte adicionado com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar esporte'}
        return context

    def form_valid(self, form):
        form_reg = form.save(commit=True)
        form_reg.administrator = self.request.user
        form_reg.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class SportEditView(MessageMixin, UpdateView):
    model = Sport
    form_class = SportForm
    template_name = 'competitions/pages/sport-create.html'
    success_url = reverse_lazy('competitions:sports:home')
    success_message = 'Esporte editado com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Editar esporte'}
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].disabled = True
        return form

    def form_valid(self, form):
        form_reg = form.save(commit=True)
        form_reg.administrator = self.request.user
        form_reg.save()
        return super().form_valid(form)


class SportDetailedView(DetailView):
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
class SportDeleteView(MessageMixin, DeleteView):
    model = Sport
    success_url = reverse_lazy('competitions:sports:home')
    success_message = 'Esporte removido com sucesso!'
    # error_message = 'Não foi possível remover este esporte'

    def get(self, request, *args, **kwargs):
        self.delete(request, *args, **kwargs)
        return redirect(self.success_url)

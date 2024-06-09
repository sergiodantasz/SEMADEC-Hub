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
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from home.views import BaseListView

from apps.competitions.forms import (
    TestForm,
    TestTeamForm,
)
from apps.competitions.models import Test, TestTeam
from apps.home.views.views import BaseSearchView, MessageMixin
from apps.teams.models import Team
from helpers.decorators import admin_required


class TestListView(BaseListView):
    model = Test
    template_name = 'competitions/pages/tests.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('-date_time')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Competições',
            'page_variant': 'tests',
        }
        return context


class TestSearchView(BaseSearchView):
    model = Test
    template_name = 'competitions/pages/competitions.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(
            Q(title__icontains=self.querystr) | Q(description__icontains=self.querystr)
        )
        return super().get_queryset(query, 'title')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Competições', 'page_variant': 'tests'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TestCreateView(MessageMixin, FormView):
    template_name = 'competitions/pages/test-create.html'
    form_class = TestForm
    success_url = reverse_lazy('competitions:tests:home')
    success_message = 'Prova adicionada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'
    error_message_teams = 'Adicione ao menos um time antes de criar uma prova.'

    def is_model_populated(self, model: Model):
        return model.objects.exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar prova'}
        return context

    def get(
        self, request, *args, **kwargs
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        if not self.is_model_populated(Team):
            messages.error(request, self.error_message_teams)
            return redirect(reverse('competitions:tests:home'))
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        form_reg = form.save(commit=True)
        form_reg.administrator = self.request.user
        form_reg.save()
        # Add success message
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TestEditView(MessageMixin, UpdateView):
    model = Test
    form_class = TestForm
    form_teams = modelformset_factory(
        TestTeam,
        TestTeamForm,
        extra=0,
        fields=['score'],
    )
    template_name = 'competitions/pages/test-edit.html'
    redirect_url = 'competitions:tests:home'
    success_message = 'Prova editada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Editar prova', 'form_teams': self.get_form_teams()}
        return context

    def get_form(self, form_class=None):
        form = self.form_class(self.request.POST or None, instance=self.get_object())
        form.fields['teams'].required = False
        return form

    def get_form_teams(self, form_class=None):
        form_teams = self.form_teams(
            self.request.POST or None,
            queryset=TestTeam.objects.filter(
                test__pk=self.get_object().pk,
            ),
        )
        return form_teams

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        self.object = self.get_object()
        form = self.get_form()
        form_teams = self.get_form_teams()
        if form.is_valid() and form_teams.is_valid():
            form.save()
            form_teams.save()
            messages.success(request, self.success_message)
        else:
            messages.error(request, self.error_message)
        return redirect(self.redirect_url)


class TestDetailView(DetailView):
    model = Test
    template_name = 'competitions/pages/test-detailed.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': self.get_object().title}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TestDeleteView(MessageMixin, DeleteView):
    model = Test
    success_url = reverse_lazy('competitions:tests:home')
    success_message = 'Prova removida com sucesso!'
    # error_message = 'Não foi possível remover esta prova'

    def get(self, request, *args, **kwargs):
        self.delete(request, *args, **kwargs)
        return redirect(self.success_url)

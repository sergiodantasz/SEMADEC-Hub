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
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, FormView, UpdateView

from apps.competitions.forms import (
    TestForm,
    TestTeamForm,
)
from apps.competitions.models import Test, TestTeam
from apps.teams.models import Team
from helpers.decorators import admin_required


class TestView(ListView):
    model = Test
    template_name = 'competitions/pages/tests.html'
    context_object_name = 'db_regs'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Test.objects.order_by('-date_time')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Competições',
            'page_variant': 'tests',
            'search_url': reverse('competitions:tests:search'),
        }
        return context


class TestSearchView(ListView):
    model = Test
    template_name = 'competitions/pages/competitions.html'
    context_object_name = 'db_regs'
    paginate_by = 10
    warning_message = 'Digite um termo de busca válido.'

    def get_search_term(self) -> str:
        return self.request.GET.get('q', '').strip()

    def get_queryset(self) -> QuerySet[Any]:
        querystr = self.get_search_term()
        if not querystr:
            messages.warning(self.request, self.warning_message)
        queryset = Test.objects.filter(
            Q(Q(title__icontains=querystr) | Q(description__icontains=querystr))
        ).order_by('title')
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        # Implement a better dict join solution
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Competições', 'page_variant': 'tests'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TestCreateView(FormView):
    template_name = 'competitions/pages/test-create.html'
    form_class = TestForm
    success_url = reverse_lazy('competitions:tests:home')
    success_message = 'Prova adicionada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'
    error_message_teams = 'Adicione ao menos um time antes de criar uma prova.'

    def is_model_populated(self, model: Model):
        return model.objects.exists()

    def get(
        self, request, *args, **kwargs
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        if not self.is_model_populated(Team):
            messages.error(request, self.error_message_teams)
            return redirect(reverse('competitions:tests:home'))
        context = {'title': 'Criar prova', 'form': self.get_form()}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        teams_m2m = form.cleaned_data['teams']
        form_reg = form.save(commit=True)
        form_reg.teams.add(*teams_m2m)
        form_reg.administrator = self.request.user
        form_reg.save()
        # Add success message
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TestEditView(UpdateView):
    model = Test
    form = TestForm
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

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        form = self.form(instance=self.object)
        form.fields['teams'].required = False
        form_teams = self.form_teams(
            queryset=TestTeam.objects.filter(
                test__pk=self.object.pk,
            )
        )
        context = {
            'title': 'Editar prova',
            'form': form,
            'form_teams': form_teams,
        }
        return render(request, self.template_name, context)

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        self.object = self.get_object()
        form = self.form(request.POST, instance=self.object)
        form.fields['teams'].required = False
        form_teams = self.form_teams(
            request.POST,
            queryset=TestTeam.objects.filter(
                test__pk=self.object.pk,
            ),
        )
        if form.is_valid() and form_teams.is_valid():
            form.save()
            form_teams.save()
            messages.success(request, self.success_message)
        else:
            messages.error(request, self.error_message)
        return redirect(self.redirect_url)


class TestDetailedView(DetailView):
    model = Test
    template_name = 'competitions/pages/test-detailed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context |= {'test': self.object}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TestDeleteView(DeleteView): ...

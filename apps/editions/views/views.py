from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db import DatabaseError
from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import HiddenInput, modelformset_factory
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

from apps.competitions.models import Sport
from apps.editions.forms import EditionForm, EditionTeamForm
from apps.editions.models import Edition, EditionTeam
from apps.teams.models import Team
from helpers.decorators import admin_required


class EditionView(ListView):
    model = Edition
    template_name = 'editions/pages/editions.html'
    context_object_name = 'db_regs'
    paginate_by = 10

    def get_queryset(self):
        return Edition.objects.order_by('-year')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edições'
        context['search_url'] = reverse('editions:editions_search')
        return context


class EditionDetailedView(DetailView):
    model = Edition
    template_name = 'editions/pages/edition-detailed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context['reg'] = self.object
        context['matches'] = self.object.matches.all()
        return context


class EditionSearchView(ListView):
    model = Edition
    template_name = 'editions/pages/editions.html'
    context_object_name = 'db_regs'
    paginate_by = 10
    warning_message = 'Digite um termo de busca válido.'

    def get_search_term(self) -> str:
        return self.request.GET.get('q', '').strip()

    def get_queryset(self) -> QuerySet[Any]:
        querystr = self.get_search_term()
        if not querystr:
            messages.warning(self.request, self.warning_message)
        queryset = Edition.objects.filter(
            Q(
                Q(year__icontains=querystr)
                | Q(name__icontains=querystr)
                | Q(edition_type__icontains=querystr)
                | Q(theme__icontains=querystr)
            )
        )
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edições'
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EditionCreateFormView(SuccessMessageMixin, FormView):
    template_name = 'editions/pages/edition-create.html'
    form_class = EditionForm
    form_error_sport = 'Adicione ao menos um esporte antes de criar uma edição.'
    form_error_team = 'Adicione ao menos um time antes de criar uma edição.'
    success_url = reverse_lazy('editions:editions')
    success_message = 'Edição adicionada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if not Sport.objects.exists():
            messages.error(self.request, self.form_error_sport)
            return redirect(self.success_url)
        if not Team.objects.exists():
            messages.error(self.request, self.form_error_team)
            return redirect(self.success_url)
        context = {'title': 'Criar edição', 'form': self.get_form()}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        teams_m2m = form.cleaned_data['teams']
        form_reg = form.save(commit=True)
        form_reg.teams.add(*teams_m2m)
        form_reg.administrator = self.request.user
        form_reg.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EditionEditFormView(UpdateView):
    model = Edition
    form = EditionForm
    form_teams = modelformset_factory(
        EditionTeam,
        EditionTeamForm,
        extra=0,
        fields=['score'],
    )
    template_name = 'editions/pages/edition-edit.html'
    redirect_url = reverse_lazy('editions:editions')
    success_message = 'Edição editada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        form = self.form(instance=self.object)
        form.fields['year'].disabled = True
        form.fields['sports'].disabled = True
        form.fields['teams'].required = False
        form.fields['teams'].widget = HiddenInput()
        form.fields['sports'].required = False
        form_teams = self.form_teams(
            queryset=EditionTeam.objects.filter(
                edition__pk=self.object.pk,
            ),
        )
        context = {
            'title': 'Editar edição',
            'form': form,
            'form_teams': form_teams,
        }
        return render(request, self.template_name, context)

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        self.object = self.get_object()
        form = self.form(request.POST, instance=self.object)
        form.fields['year'].disabled = True
        form.fields['sports'].disabled = True
        form.fields['teams'].required = False
        form.fields['teams'].widget = HiddenInput()
        form.fields['sports'].required = False
        form_teams = self.form_teams(
            request.POST,
            queryset=EditionTeam.objects.filter(
                edition__pk=self.object.pk,
            ),
        )
        if form.is_valid() and form_teams.is_valid():
            form.save()
            form_teams.save()
            messages.success(self.request, self.success_message)
        else:
            messages.error(request, self.error_message)
        return redirect(self.redirect_url)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EditionDeleteView(DeleteView):
    model = Edition
    success_url = reverse_lazy('editions:editions')
    success_message = 'Edição removida com sucesso!'
    error_message = 'Não foi possível remover esta edição.'

    def get(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
        except DatabaseError:
            messages.error(request, self.error_message)
        else:
            messages.success(request, self.success_message)
        return redirect(self.success_url)

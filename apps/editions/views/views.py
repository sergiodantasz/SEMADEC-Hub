from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db import DatabaseError
from django.db.models import Model, Q
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
from home.views import MessageMixin

from apps.competitions.models import Sport
from apps.competitions.tests.factories import SportFactory
from apps.editions.forms import EditionForm, EditionTeamForm
from apps.editions.models import Edition, EditionTeam
from apps.teams.models import Team
from apps.teams.tests.factories import ClassFactory, CourseFactory, TeamFactory
from helpers.decorators import admin_required


class EditionListView(ListView):
    model = Edition
    template_name = 'editions/pages/editions.html'
    context_object_name = 'db_regs'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Edition.objects.order_by('-year')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Edições',
            'search_url': reverse('editions:editions_search'),
        }
        return context


class EditionDetailView(DetailView):
    model = Edition
    template_name = 'editions/pages/edition-detailed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context |= {'reg': self.object, 'matches': self.object.matches.all()}
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
        context |= {'title': 'Edições'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EditionCreateView(MessageMixin, FormView):
    template_name = 'editions/pages/edition-create.html'
    form_class = EditionForm
    error_message_sport = 'Adicione ao menos um esporte antes de criar uma edição.'
    error_message_team = 'Adicione ao menos um time antes de criar uma edição.'
    success_url = reverse_lazy('editions:editions')
    success_message = 'Edição adicionada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def is_model_populated(self, model: Model):
        return model.objects.exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar edição'}
        return context

    def get(self, request, *args, **kwargs) -> HttpResponse:
        # Remove later
        # sport = SportFactory()
        # cursos = CourseFactory()
        # class1 = ClassFactory(course=cursos)
        # time = TeamFactory(classes=(class1,))
        # Remove later
        if not self.is_model_populated(Sport):
            # Change for a better message displaying
            messages.error(self.request, self.error_message_sport)
            return redirect(self.success_url)
        if not self.is_model_populated(Team):
            # Change for a better message displaying
            messages.error(self.request, self.error_message_team)
            return redirect(self.success_url)
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        form_reg = form.save(commit=True)
        form_reg.administrator = self.request.user
        form_reg.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EditionEditView(MessageMixin, UpdateView):
    model = Edition
    form_class = EditionForm
    form_teams = modelformset_factory(
        EditionTeam,
        EditionTeamForm,
        extra=0,
        fields=['score'],
    )
    template_name = 'editions/pages/edition-edit.html'
    redirect_url = reverse_lazy('editions:editions')  # Change to success_url
    success_message = 'Edição editada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Editar edição',
            'form_teams': self.get_form_teams(),
        }
        return context

    def get_form_teams(self, form_class=None):
        form_teams = self.form_teams(
            self.request.POST or None,
            queryset=EditionTeam.objects.filter(
                edition__pk=self.get_object().pk,
            ),
        )
        return form_teams

    def get_form(self, form_class=None):
        form = self.form_class(self.request.POST or None, instance=self.get_object())
        form.fields['year'].disabled = True
        form.fields['sports'].disabled = True
        form.fields['teams'].required = False
        form.fields['teams'].widget = HiddenInput()
        form.fields['sports'].required = False
        return form

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        form = self.get_form()
        form_teams = self.get_form_teams()
        if form.is_valid() and form_teams.is_valid():
            form.save()
            form_teams.save()
            messages.success(self.request, self.success_message)
        else:
            messages.error(request, self.error_message)
        return redirect(self.redirect_url)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class EditionDeleteView(MessageMixin, DeleteView):
    model = Edition
    success_url = reverse_lazy('editions:editions')
    success_message = 'Edição removida com sucesso!'
    # error_message = 'Não foi possível remover esta edição.'

    def get(self, request, *args, **kwargs):
        self.delete(request, *args, **kwargs)
        return redirect(self.success_url)

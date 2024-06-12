from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Model, Q
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
    MatchForm,
    MatchTeamForm,
)
from apps.competitions.models import Match, MatchTeam
from apps.editions.models import Edition
from apps.teams.models import Team
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseEditView,
    MessageMixin,
)
from helpers.decorators import admin_required


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MatchCreateView(BaseCreateView):
    form_class = MatchForm
    template_name = 'competitions/pages/match-create.html'
    msg = {
        'success': {'form': 'Partida adicionada com sucesso.'},
        'error': {
            'form': 'Preencha os campos do formulário corretamente.',
            'team': 'Adicione ao menos um time antes de criar uma prova.',
        },
    }

    def is_model_populated(self, model: Model):
        return model.objects.exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar partida'}
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('editions:detailed', kwargs={'pk': self.get_object_pk()})

    def get(
        self, request, *args, **kwargs
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        if not self.is_model_populated(Team):
            messages.error(request, self.msg['error']['team'])
            return redirect(self.get_success_url())
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        edition_obj = Edition.objects.get(pk=self.get_object_pk())
        form_reg = form.save(commit=False)
        form_reg.edition = edition_obj
        form_reg.save()
        form.save_m2m()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MatchEditView(BaseEditView):
    form_class = MatchForm
    form_matches = modelformset_factory(
        MatchTeam,
        MatchTeamForm,
        extra=0,
        fields=['score'],
    )
    template_name = 'competitions/pages/match-edit.html'
    msg = {
        'success': {'form': 'Partida editada com sucesso.'},
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_success_url(self) -> str:
        return reverse_lazy(
            'editions:detailed', kwargs={'pk': self.get_object().edition.pk}
        )

    def get_form(self, form_class=None):
        form = self.form_class(self.request.POST or None, instance=self.get_object())
        form.fields['sport_category'].disabled = True
        form.fields['teams'].disabled = True
        return form

    def get_form_matches(self, form_class=None):
        form_matches = self.form_matches(
            self.request.POST or None,
            queryset=MatchTeam.objects.filter(match__pk=self.object.pk),
        )
        return form_matches

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Editar partida',
            'form_matches': self.get_form_matches(),
        }
        return context

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        self.object = self.get_object()
        form = self.get_form()
        form_matches = self.get_form_matches()
        if form.is_valid() and form_matches.is_valid():
            form.save()
            form_matches.save()
            messages.success(request, self.msg['success']['form'])
        else:
            messages.error(request, self.msg['error']['form'])
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MatchDeleteView(BaseDeleteView):
    model = Match
    msg = {
        'success': {'form': 'Partida removida com sucesso!'},
        'error': {'form': 'Não foi possível remover esta partida.'},
    }

    def get_success_url(self) -> str:
        return reverse_lazy(
            'editions:detailed', kwargs={'pk': self.get_object().edition.pk}
        )

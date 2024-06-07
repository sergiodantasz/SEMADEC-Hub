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
from apps.home.views.views import MessageMixin
from apps.teams.models import Team
from helpers.decorators import admin_required


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MatchCreateView(FormView):
    template_name = 'competitions/pages/match-create.html'
    form_class = MatchForm
    # success_url = reverse_lazy('editions:editions_detailed')
    success_message = 'Partida adicionada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'
    error_message_teams = 'Adicione ao menos um time antes de criar uma prova.'

    def get_object_pk(self):
        return self.kwargs.get('pk', '')

    def is_model_populated(self, model: Model):
        return model.objects.exists()

    def get_success_url(self) -> str:
        return reverse_lazy(
            'editions:editions_detailed', kwargs={'pk': self.get_object_pk()}
        )

    def get(
        self, request, *args, **kwargs
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        if not self.is_model_populated(Team):
            messages.error(request, self.error_message_teams)
            return redirect(reverse('editions:editions'))
        context = {'title': 'Criar partida', 'form': self.get_form()}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        edition_obj = Edition.objects.get(pk=self.get_object_pk())
        form_reg = form.save(commit=False)
        form_reg.edition = edition_obj
        form_reg.save()
        form.save_m2m()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MatchEditView(UpdateView):
    model = Match
    form = MatchForm
    form_matches = modelformset_factory(
        MatchTeam,
        MatchTeamForm,
        extra=0,
        fields=['score'],
    )
    template_name = 'competitions/pages/match-edit.html'
    # success_url = reverse_lazy('editions:editions_detailed')
    success_message = 'Partida editada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_object_pk(self):
        return self.kwargs.get('pk', '')

    def is_model_populated(self, model: Model):
        return model.objects.exists()

    def get_success_url(self) -> str:
        return reverse_lazy(
            'editions:editions_detailed', kwargs={'pk': self.get_object().edition.pk}
        )

    def get(
        self, request, *args, **kwargs
    ) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
        self.object = self.get_object()
        form = self.form(instance=self.object)
        form.fields['sport_category'].disabled = True
        form.fields['teams'].disabled = True
        form_matches = self.form_matches(
            queryset=MatchTeam.objects.filter(match__pk=self.object.pk)
        )
        context = {
            'title': 'Editar partida',
            'form': form,
            'form_matches': form_matches,
        }
        return render(request, self.template_name, context)

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        self.object = self.get_object()
        form = self.form(request.POST, instance=self.object)
        form.fields['sport_category'].disabled = True
        form.fields['teams'].disabled = True
        form_matches = self.form_matches(
            request.POST, queryset=MatchTeam.objects.filter(match__pk=self.object.pk)
        )
        if form.is_valid() and form_matches.is_valid():
            form.save()
            form_matches.save()
            messages.success(request, self.success_message)
        else:
            messages.error(request, self.error_message)
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MatchDeleteView(MessageMixin, DeleteView):
    model = Match
    success_message = 'Partida removida com sucesso!'
    # error_message = 'Não foi possível remover esta partida'

    def get_success_url(self) -> str:
        return reverse_lazy(
            'editions:editions_detailed', kwargs={'pk': self.get_object().edition.pk}
        )

    def get(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.delete(request, *args, **kwargs)
        return redirect(success_url)

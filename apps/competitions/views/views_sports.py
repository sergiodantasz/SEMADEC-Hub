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

from apps.competitions.forms import (
    SportForm,
)
from apps.competitions.models import Sport
from apps.competitions.tests.factories import CategoryFactory
from apps.editions.models import Edition
from helpers.decorators import admin_required


class SportView(ListView):
    model = Sport
    template_name = 'competitions/pages/competitions.html'
    context_object_name = 'db_regs'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return Sport.objects.order_by('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        # Remove later
        cat_masculino = CategoryFactory(name='Masculino')
        cat_feminino = CategoryFactory(name='Feminino')
        cat_misto = CategoryFactory(name='Misto')
        # Remove later
        context = super().get_context_data(**kwargs)
        context['title'] = 'Competições'
        context['page_variant'] = 'sports'
        context['search_url'] = reverse('competitions:sports:search')
        return context


class SportSearchView(ListView):
    model = Sport
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
        queryset = Sport.objects.filter(name__icontains=querystr).order_by('name')
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Competições'
        context['page_variant'] = 'sports'
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class SportCreateView(FormView):
    template_name = 'competitions/pages/sport-create.html'
    form_class = SportForm
    # Add error for non existing categories
    success_url = reverse_lazy('competitions:sports:home')
    success_message = 'Esporte adicionado com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = {'title': 'Criar esporte', 'form': self.get_form()}
        return render(request, self.template_name, context)

    def form_valid(self, form):
        cats_m2m = form.cleaned_data['categories']
        form_reg = form.save(commit=True)
        form_reg.categories.add(*cats_m2m)
        form_reg.administrator = self.request.user
        form_reg.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class SportEditView(UpdateView):
    model = Sport
    form = SportForm
    template_name = 'competitions/pages/sport-create.html'
    redirect_url = 'competitions:sports:home'
    success_message = 'Esporte editado com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        form = self.form(instance=self.object)
        form.fields['name'].disabled = True
        context = {'title': 'Editar esporte', 'form': form}
        return render(request, self.template_name, context)

    def post(
        self, request, *args, **kwargs
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        self.object = self.get_object()
        form = self.form(request.POST, instance=self.object)
        form.fields['name'].disabled = True
        if form.is_valid():
            cats_m2m = form.cleaned_data['categories']
            form_reg = form.save(commit=True)
            form_reg.categories.add(*cats_m2m)
            form_reg.administrator = request.user
            form_reg.save()
            messages.success(self.request, self.success_message)
        else:
            messages.error(request, self.error_message)
        return redirect(self.redirect_url)


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
        context['title'] = self.object.name
        context['sport_name'] = self.object.name
        context['regs'] = editions_matches
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class SportDeleteView(DeleteView): ...

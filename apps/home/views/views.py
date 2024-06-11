from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, UpdateView

from apps.home.forms import TagForm
from apps.home.models import Tag
from helpers.decorators import admin_required


class MessageMixin:
    success_message = ''
    error_message = ''
    warning_message = ''
    msg = {
        'success': dict(),
        'error': dict(),
    }

    def is_model_populated(self, model):
        if self.success_message:
            messages.success(self.request, self.success_message)
        elif self.error_message:
            messages.success(self.request, self.error_message)
        return model.objects.exists()

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response

    def get_queryset(self):
        response = super().get_queryset()
        if self.warning_message:
            messages.warning(self.request, self.warning_message)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        elif msg := self.msg['success'].get('form', ''):
            messages.success(self.request, msg)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.error_message:
            messages.error(self.request, self.error_message)
        elif msg := self.msg['error'].get('form', ''):
            messages.error(self.request, msg)
        return response


class BaseListView(ListView):
    context_object_name = 'db_regs'

    def get_queryset(self, ordering: str) -> QuerySet[Any]:
        return self.model.objects.order_by(ordering)

    def get_app_name(self) -> str:
        return self.request.resolver_match.app_name

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'search_url': reverse(f'{self.get_app_name()}:search')}
        return context


class BaseSearchView(MessageMixin, ListView):
    context_object_name = 'db_regs'
    warning_message = 'Digite um termo de busca válido.'

    def get_search_term(self) -> str:
        self.querystr = self.request.GET.get('q', '').strip()
        return self.querystr

    def get_queryset(self, query: Q, ordering: str) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        if not self.querystr:
            messages.warning(self.request, self.warning_message)

        queryset = self.model.objects.filter(query).order_by(ordering)
        return queryset


class BaseFormView(MessageMixin, FormView):
    msg = {
        'success': dict(),
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_app_name(self) -> str:
        return self.request.resolver_match.app_name

    def get_success_url(self) -> str:
        return reverse_lazy(f'{self.get_app_name()}:home')

    def get_object_pk(self):
        return self.kwargs.get('pk', '')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BaseCreateView(BaseFormView):
    def is_model_populated(self, model: Model):
        return model.objects.exists()


class BaseEditView(BaseFormView, UpdateView):
    pass


def home(request):
    context = {'title': 'Início'}
    return render(request, 'home/pages/home.html', context)


def tags(request):
    tags_objs = Tag.objects.order_by('name')
    context = {
        'title': 'Tags',
        'tags': tags_objs,
    }
    return render(request, 'home/pages/tags.html', context)


@login_required
@admin_required
def tags_create(request):
    form = TagForm(request.POST or None)
    context = {
        'title': 'Criar tag',
        'form': form,
    }
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag criada com sucesso.')
            return redirect(reverse('home:tags'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'home/pages/create-tag.html', context)


@login_required
@admin_required
def tags_delete(request, slug):
    tag_obj = get_object_or_404(Tag, slug=slug)
    tag_obj.delete()
    messages.success(request, 'Tag apagada com sucesso.')
    return redirect(reverse('home:tags'))

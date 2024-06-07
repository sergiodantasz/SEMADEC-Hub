from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView
from home.views import BaseListView, MessageMixin

from apps.teams.forms import ClassForm
from apps.teams.models import Class, Course
from helpers.decorators import admin_required


class ClassListView(BaseListView):
    model = Class
    template_name = 'teams/pages/classes.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {
            'title': 'Turmas',
        }
        return context


class ClassSearchView(MessageMixin, ListView):
    model = Class
    template_name = 'teams/pages/classes.html'
    context_object_name = 'db_regs'
    warning_message = 'Digite um termo de busca válido.'

    def get_search_term(self) -> str:
        return self.request.GET.get('q', '').strip()

    def get_queryset(self) -> QuerySet[Any]:
        querystr = self.get_search_term()
        # Test with MessageMixin
        if not querystr:  # Remove later
            messages.warning(self.request, self.warning_message)
        queryset = Class.objects.filter(
            Q(
                Q(name__icontains=querystr) | Q(course__name__icontains=querystr),
            )
        ).order_by('name')
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Turmas'}
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ClassCreateView(MessageMixin, FormView):
    form_class = ClassForm
    template_name = 'teams/pages/class-create.html'
    success_url = reverse_lazy('teams:classes:home')
    success_message = 'Turma adicionada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'
    error_message_course = 'Adicione ao menos um curso antes de criar uma turma.'

    def is_model_populated(self, model: Model):
        return model.objects.exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Criar turma'}
        return context

    def get(self, request, *args, **kwargs):
        if not self.is_model_populated(Course):
            messages.error(self.request, self.error_message_course)
            return redirect(self.success_url)
        context = self.get_context_data()
        return self.render_to_response(context)

    def form_valid(self, form):
        form_reg = form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ClassEditView(MessageMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = 'teams/pages/class-create.html'
    success_url = reverse_lazy('teams:classes:home')
    success_message = 'Turma editada com sucesso.'
    error_message = 'Preencha os campos do formulário corretamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'title': 'Editar turma'}
        return context

    def form_valid(self, form):
        form_reg = form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ClassDeleteView(MessageMixin, DeleteView):
    model = Class
    success_url = reverse_lazy('teams:classes:home')
    success_message = 'Turma removida com sucesso!'

    def get(self, request, *args, **kwargs):
        self.delete(request, *args, **kwargs)
        return redirect(self.success_url)

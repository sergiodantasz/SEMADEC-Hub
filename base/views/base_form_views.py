from typing import Any

from django.db.models import Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView, UpdateView

from .message_mixin import MessageMixin


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

    def get_queryset(self) -> QuerySet[Any]:
        return (
            super().get_queryset()
            if self.model
            else self.form_class._meta.model.objects.all()
        )

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BaseCreateView(BaseFormView):
    def is_model_populated(self, model: Model):
        return model.objects.exists()


class BaseEditView(BaseFormView, UpdateView): ...


class BaseDeleteView(BaseFormView, DeleteView):
    def get(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.delete(request, *args, **kwargs)
        return redirect(success_url)

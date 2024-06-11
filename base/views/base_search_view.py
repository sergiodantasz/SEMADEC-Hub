from typing import Any

from django.contrib import messages
from django.db.models import Model, Q
from django.db.models.query import QuerySet
from django.views.generic import ListView

from apps.home.forms import TagForm
from apps.home.models import Tag
from helpers.decorators import admin_required

from .message_mixin import MessageMixin


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

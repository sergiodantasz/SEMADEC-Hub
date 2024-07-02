from typing import Any

from django.db.models.query import QuerySet
from django.urls import NoReverseMatch, reverse
from django.views.generic import ListView


class BaseListView(ListView):
    context_object_name = 'db_regs'

    def get_queryset(self, ordering: str) -> QuerySet[Any]:
        return self.model.objects.order_by(ordering)

    def get_app_name(self) -> str:
        return self.request.resolver_match.app_name

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            context |= {'search_url': reverse(f'{self.get_app_name()}:search')}
        except NoReverseMatch:
            pass
        finally:
            return context

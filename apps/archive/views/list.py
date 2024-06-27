from typing import Any

from django.contrib import messages
from django.db.models import Q
from django.db.models.query import QuerySet
from django.views.generic.list import ListView

from apps.home.models import Collection
from base.views.base_search_view import BaseSearchView
from helpers.pagination import make_pagination


class ArchiveListView(ListView):
    model = Collection
    context_object_name = 'db_regs'
    ordering = '-created_at'
    template_name = 'archive/pages/archive_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_obj, pagination_range, paginator = make_pagination(
            self.request, context.get('db_regs'), 15
        )
        context |= {
            'title': 'Acervo',
            'search_url': '',
            'db_regs': page_obj,
            'pagination_range': pagination_range,
        }
        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(collection_type='image')
        return queryset


class ArchiveSearchView(BaseSearchView):
    model = Collection
    template_name = 'archive/pages/archive_list.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(title__icontains=self.querystr)
        return super().get_queryset(query, 'title')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = {'title': 'Acervo'}
        return super().get_context_data(**context)

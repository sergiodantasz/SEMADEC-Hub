from typing import Any

from django.db.models import Q
from django.db.models.query import QuerySet

from apps.home.models import Collection
from base.views.base_list_view import BaseListView
from base.views.base_search_view import BaseSearchView


class ArchiveListView(BaseListView):
    model = Collection
    template_name = 'archive/pages/archive_list.html'
    ordering = '-created_at'
    paginate_by = 2  # Change later

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {'title': 'Acervo', 'search_url': ''}
        return super().get_context_data(**context)

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset(ordering=self.ordering)  # type: ignore
        queryset = queryset.filter(collection_type='image')
        return queryset


class ArchiveSearchView(BaseSearchView):
    model = Collection
    template_name = 'archive/pages/archive_list.html'
    paginate_by = 2  # Change later

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(title__icontains=self.querystr)
        return super().get_queryset(query, 'title')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = {'title': 'Acervo'}
        return super().get_context_data(**context)

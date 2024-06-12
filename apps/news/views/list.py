from typing import Any, Iterable

from django.db.models import Count, Q
from django.db.models.query import QuerySet

from apps.home.models import Tag
from apps.news.models import News
from apps.news.tests.factories import NewsFactory
from base.views import BaseListView, BaseSearchView
from helpers.pagination import make_pagination


class NewsListView(BaseListView):
    model = News
    template_name = 'news/pages/news_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('-created_at')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_obj, pagination_range, paginator = make_pagination(
            self.request, context.get('db_regs'), 10
        )
        context |= {
            'title': 'Notícias',
            'db_regs': page_obj,  # Remove later
            'pagination_range': pagination_range,
        }
        return context


class NewsSearchView(BaseSearchView):
    model = News
    template_name = 'news/pages/news_search.html'

    def get_tags_from_url(self) -> list[str | Any]:
        return self.request.GET.get('tags', '').split(',')

    def get_tags(self, tags: Iterable[str | Any]):
        tags = [item.strip() for item in tags if item != '']
        tags = set(tags)
        tags = Tag.objects.filter(slug__in=tags).order_by('name')
        return tags

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        query = Q(
            Q(title__icontains=self.querystr)
            | Q(excerpt__icontains=self.querystr)
            | Q(content__icontains=self.querystr)
            | Q(tags__name__icontains=self.querystr)
        )
        # queryset = super().get_queryset()
        # if self.querystr:
        #     queryset = queryset.filter(
        #         Q(title__icontains=search_term)
        #         | Q(excerpt__icontains=search_term)
        #         | Q(content__icontains=search_term)
        #     )
        # tags = self.get_tags(self.get_tags_from_url())
        # if tags:
        #     queryset = (
        #         queryset.filter(tags__in=tags)
        #         .annotate(tags_count=Count('tags'))
        #         .filter(tags_count=len(tags))
        #         .distinct()
        #     )
        return super().get_queryset(query, '-created_at')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_term = self.get_search_term()
        page_obj, pagination_range, paginator = make_pagination(
            self.request, context.get('db_regs'), 10
        )
        context |= {
            'title': 'Pesquisa - Notícias',
            'search_term': search_term,
            'tags': self.get_tags(self.get_tags_from_url()),
            'db_regs': page_obj,
            'pagination_range': pagination_range,
            'paginator': paginator,
            'additional_url_params': f'&q={search_term}',
        }
        return context

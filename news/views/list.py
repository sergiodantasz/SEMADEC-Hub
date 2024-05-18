from typing import Any, Iterable

from django.db.models import Count, Q
from django.db.models.query import QuerySet
from django.urls import reverse
from django.views.generic.list import ListView

from helpers.pagination import make_pagination
from home.models import Tag
from news.models import News


class BaseNewsListView(ListView):
    model = News
    context_object_name = 'news_list'
    ordering = '-created_at'


class NewsListView(BaseNewsListView):
    template_name = 'news/pages/news_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notícias'
        context['search_url'] = reverse('news:search')
        page_obj, pagination_range, paginator = make_pagination(
            self.request, context.get('news_list'), 10
        )
        context['news_list'] = page_obj
        context['pagination_range'] = pagination_range
        return context


class NewsSearchListView(BaseNewsListView):
    template_name = 'news/pages/news_search.html'

    def get_search_term(self) -> str:
        return self.request.GET.get('q', '')

    def get_tags_from_url(self) -> list[str | Any]:
        return self.request.GET.get('tags', '').split(',')

    def get_tags(self, tags: Iterable[str | Any]):
        tags = [item.strip() for item in tags if item != '']
        tags = set(tags)
        tags = Tag.objects.filter(slug__in=tags).order_by('name')
        return tags

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        search_term = self.get_search_term()
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term)
                | Q(excerpt__icontains=search_term)
                | Q(content__icontains=search_term)
            )
        tags = self.get_tags(self.get_tags_from_url())
        if tags:
            queryset = (
                queryset.filter(tags__in=tags)
                .annotate(tags_count=Count('tags'))
                .filter(tags_count=len(tags))
                .distinct()
            )
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pesquisa - Notícias'
        context['search_url'] = reverse('news:search')
        search_term = self.get_search_term()
        context['search_term'] = search_term
        context['tags'] = self.get_tags(self.get_tags_from_url())
        page_obj, pagination_range, paginator = make_pagination(
            self.request, context.get('news_list'), 10
        )
        context['news_list'] = page_obj
        context['pagination_range'] = pagination_range
        context['paginator'] = paginator
        context['additional_url_params'] = f'&q={search_term}'
        return context

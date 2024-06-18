from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.list import ListView

from apps.archive.forms import ImageCollectionForm, ImageForm
from apps.archive.models import Image
from apps.archive.tests.factories import CollectionArchiveFactory
from apps.home.models import Collection
from helpers.decorators import admin_required
from helpers.model import is_owner
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
from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.editions.models import Edition
from apps.home.forms import TagForm
from apps.home.models import Collection, Tag
from apps.news.models import News
from base.views.base_form_views import BaseCreateView, BaseDeleteView
from base.views.base_list_view import BaseListView
from helpers.decorators import admin_required


class HomeView(TemplateView):
    template_name = 'home/pages/home.html'

    def get_context_data(self, **kwargs):
        last_edition = Edition.objects.order_by('-year').first()
        context = {
            'title': 'Início',
            'last_edition': last_edition or '',
            'news_regs': News.objects.order_by('-created_at')[:4],
            'document_reg': Collection.objects.filter(collection_type='document')
            .order_by('-created_at')
            .first()
            or '',
            'archive_reg': Collection.objects.filter(collection_type='image')
            .order_by('-created_at')
            .first(),
            'matches_regs': ''
            if not last_edition
            else last_edition.get_matches.order_by('-date_time')[:10],
        }
        return super().get_context_data(**context)


class TagListView(BaseListView):
    model = Tag
    template_name = 'home/pages/tags.html'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset('name')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = {'title': 'Tags'}
        return super().get_context_data(**context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TagCreateView(BaseCreateView):
    form_class = TagForm
    template_name = 'home/pages/create-tag.html'
    msg = {
        'success': {'form': 'Tag criada com sucesso.'},
        'error': {'form': 'Preencha os campos do formulário corretamente.'},
    }

    def get_context_data(self, **kwargs):
        context = {'title': 'Criar tag'}
        return super().get_context_data(**context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class TagDeleteView(BaseDeleteView):
    model = Tag
    msg = {
        'success': {'form': 'Tag apagada com sucesso.'},
        'error': {'form': 'Não foi possível remover esta tag.'},
    }

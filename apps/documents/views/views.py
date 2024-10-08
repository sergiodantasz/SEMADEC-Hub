from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from apps.documents.forms import DocumentCollectionForm, DocumentForm
from apps.documents.models import Document
from apps.home.models import Collection
from base.views.base_form_views import BaseCreateView, BaseDeleteView, BaseEditView
from base.views.base_list_view import BaseListView
from base.views.base_search_view import BaseSearchView
from helpers.decorators import admin_required
from helpers.model import is_owner


class DocumentListView(BaseListView):
    model = Collection
    template_name = 'documents/pages/documents_list.html'
    ordering = '-created_at'
    paginate_by = 2  # Change later

    def get_context_data(self, **kwargs):
        context = {
            'title': 'Documentos',
            'search_url': reverse('documents:search'),
        }
        return super().get_context_data(**context)

    def get_queryset(self):
        queryset = super().get_queryset(ordering=self.ordering)  # type: ignore
        queryset = queryset.filter(collection_type='document')
        return queryset


class DocumentSearchView(BaseSearchView):
    model = Collection
    template_name = 'documents/pages/documents_list.html'
    paginate_by = 2  # Change later

    def get_queryset(self) -> QuerySet[Any]:
        self.querystr = self.get_search_term()
        ### CHANGE QUERY ###
        query = Q(
            Q(collection_type__iexact='document')
            & Q(
                Q(title__icontains=self.querystr)
                | Q(documents__name__icontains=self.querystr)
                # Add document display name
            )
        )
        return super().get_queryset(query, 'title')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = {'title': 'Documentos'}
        return super().get_context_data(**context)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class DocumentCreateView(BaseCreateView):
    form_class = DocumentCollectionForm
    document_form = DocumentForm
    template_name = 'documents/pages/document_form.html'
    msg = {
        'success': {'form': 'Coleção de documentos criada com sucesso.'},
        'error': {
            'form': 'Preencha os campos do formulário corretamente.',
            'documents': 'Nenhum documento foi selecionado.',
        },
    }

    def get_document_form(self, form_class=None):
        document_form = self.document_form(
            self.request.POST or None, self.request.FILES or None
        )
        return document_form

    def get_context_data(self, **kwargs):
        context = {
            'title': 'Criar coleção de documentos',
            'document_form': self.get_document_form(),
        }
        return super().get_context_data(**context)

    def form_valid(self, form):
        document_form = self.get_document_form()
        if document_form.is_valid():
            documents = self.request.FILES.getlist('documents')
            names = [
                name
                for item, name in self.request.POST.items()
                if item.startswith('document-')
            ]
            if not documents or not names:
                messages.error(self.request, self.msg['error']['documents'])
                return self.form_invalid(form)
            document_collection = form.save(commit=False)  # type: ignore
            document_collection.administrator = self.request.user
            document_collection.save()
            form.save_m2m()  # type: ignore
            for i, document in enumerate(documents):
                Document.objects.create(
                    collection=document_collection,
                    name=names[i],
                    content=document,
                )
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class DocumentDeleteView(BaseDeleteView):
    model = Collection
    msg = {
        'success': {'form': 'Coleção de documentos apagada com sucesso.'},
        'error': {'form': 'Não foi possível apagar esta coleção de documentos.'},
    }

    def get(self, request, *args, **kwargs):
        if not is_owner(request.user, self.get_object()):  # type: ignore
            messages.error(request, self.msg['error']['form'])
        else:
            self.delete(request, *args, **kwargs)
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class DocumentEditView(BaseEditView):
    form_class = DocumentCollectionForm
    document_form = DocumentForm
    template_name = 'documents/pages/document_form.html'
    msg = {
        'success': {'form': 'Coleção de documentos editada com sucesso.'},
        'error': {
            'form': 'Preencha os campos do formulário corretamente.',
            'image': 'Nenhum arquivo foi selecionado.',
        },
    }

    def get_document_form(self, form_class=None):
        document_form = self.document_form(
            self.request.POST or None, self.request.FILES or None
        )
        return document_form

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {
            'title': 'Editar coleção de documentos',
            'document_form': self.get_document_form(),
            'is_editing': True,
        }
        return super().get_context_data(**context)

    def form_valid(self, form):
        document_form = self.get_document_form()
        if document_form.is_valid():
            documents = self.request.FILES.getlist('documents')
            names = [
                name
                for item, name in self.request.POST.items()
                if item.startswith('document-')
            ]
            documents_to_remove_ids = [
                k.split('-')[-1]
                for k, v in self.request.POST.items()
                if k.startswith('document-') and v == 'yes'
            ]
            document_collection = form.save()  # type: ignore
            for i, document in enumerate(documents):
                Document.objects.create(
                    collection=document_collection,
                    name=names[i],
                    content=document,
                )
            for document_id in documents_to_remove_ids:
                document = Document.objects.get(id=document_id)
                document.delete()
            if not document_collection.get_documents.exists():
                document_collection.delete()  # Not working
                messages.success(
                    self.request, 'Coleção de documentos apagada com sucesso.'
                )
            # Conflito entre o "name" dos inputs
        return super().form_valid(form)

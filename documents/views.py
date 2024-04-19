from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from documents.forms import DocumentCollectionForm, DocumentForm
from documents.models import Document
from documents.tests.factories import CollectionDocumentsFactory, DocumentFactory
from helpers.decorators import admin_required
from helpers.model import is_owner
from home.models import Collection

# from archive.tests.factories import CollectionFactory, DocumentFactory
# from home.tests.factories import CollectionFactory


def documents_collection(request):
    # collection_fac = CollectionDocumentsFactory()  # Remove if needed
    # DocumentFactory.create_batch(
    #     size=3,
    #     collection=collection_fac,
    # )  # Remove if needed
    documents_collection_objs = Collection.objects.filter(
        collection_type='document'
    ).order_by('-updated_at')
    context = {
        'title': 'Documentos',
        'db_regs': documents_collection_objs,
    }
    return render(request, 'documents/pages/documents.html', context)


def search_document_collection(request):
    query = request.GET.get('q').strip()
    if not query:
        return redirect(reverse('documents:documents'))
    search = Collection.objects.filter(  # CHANGE
        Q(
            Q(collection_type__iexact='document')
            & Q(
                Q(title__icontains=query),
            )
        ),
    )
    context = {
        'title': 'Documentos',
        'db_regs': search,
    }
    return render(request, 'documents/pages/documents.html', context)


@login_required
@admin_required
def create_document_collection(request):
    form = DocumentCollectionForm(request.POST or None, request.FILES or None)
    document_form = DocumentForm(request.POST or None, request.FILES or None)
    context = {
        'title': 'Criar coleção de documentos',
        'form': form,
        'document_form': document_form,
        'form_action': reverse('documents:create_document'),
    }
    if request.POST:
        documents = request.FILES.getlist('documents')
        names = [
            name for item, name in request.POST.items() if item.startswith('document-')
        ]
        if form.is_valid():
            if not documents or not names:
                messages.error(request, 'Nenhum documento foi selecionado.')
            else:
                document_collection = form.save(commit=False)
                document_collection.administrator = request.user
                document_collection.save()
                for i, document in enumerate(documents):
                    Document.objects.create(
                        collection=document_collection,
                        name=names[i],
                        content=document,
                    )
                messages.success(request, 'Coleção de documentos criada com sucesso.')
                return redirect(reverse('documents:documents'))
        else:
            messages.error(request, 'Preencha os campos do formulário corretamente.')
    return render(request, 'documents/pages/create-document.html', context)


@login_required
@admin_required
def delete_document_collection(request, slug):
    document_collection_obj = get_object_or_404(
        Collection, collection_type='document', slug=slug
    )
    if not is_owner(request.user, document_collection_obj):
        raise PermissionDenied()
    document_collection_obj.delete()
    messages.success(request, 'Coleção de documentos apagada com sucesso.')
    return redirect(reverse('documents:documents'))

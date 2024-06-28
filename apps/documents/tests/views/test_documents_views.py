from django.urls import resolve, reverse

from apps.documents import views


def test_documents_viewname_redirects_to_documents_view():
    view = resolve(reverse('documents:home'))
    assert view.func is views.documents_collection


def test_documents_search_viewname_redirects_to_documents_search_view():
    view = resolve(reverse('documents:search'))
    assert view.func is views.search_document_collection

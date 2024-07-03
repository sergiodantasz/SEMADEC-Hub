from django.contrib.messages import get_messages
from django.db.models.query import QuerySet
from django.test import Client, RequestFactory
from django.urls import resolve, reverse

from apps.archive.tests.factories import CollectionArchiveFactory
from apps.documents import views
from apps.documents.forms import DocumentCollectionForm, DocumentForm
from apps.users.tests.factories import UserFactory


def test_documents_list_view_get_queryset_method_returns_queryset():
    view = views.DocumentListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_documents_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('documents:home'))
    request.resolver_match = resolve(reverse('documents:home'))
    response = views.DocumentListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_documents_search_view_get_queryset_method_returns_queryset(db):
    request = RequestFactory().get(reverse('documents:search'))
    request.GET |= {'q': 'test'}
    view = views.DocumentSearchView()
    view.setup(request)
    queryset = view.get_queryset()
    assert isinstance(queryset, QuerySet)


def test_documents_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('documents:search'))
    request.GET |= {'q': 'test'}
    response = views.DocumentSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_documents_create_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('documents:create'))
    request.resolver_match = resolve(reverse('documents:create'))
    request.user = UserFactory(is_admin=True)
    response = views.DocumentCreateView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_documents_create_view_get__document_form_returns_form(db):
    request = RequestFactory().get(reverse('documents:create'))
    view = views.DocumentCreateView()
    view.setup(request)
    form = view.get_document_form()
    assert isinstance(form, DocumentForm)


def test_documents_create_post_method_returns_status_code_200(db):
    c = Client()
    request = c.get(reverse('documents:create')).wsgi_request
    view = views.DocumentCreateView()
    view.setup(request)
    response = view.post(request)
    assert response.status_code == 200


def test_documents_create_view_form_valid_redirects_to_documents_home(
    db, document_collection_form_fixture
):
    c = Client()
    user = UserFactory()
    request = c.get(reverse('documents:create')).wsgi_request
    request.user = user
    form = document_collection_form_fixture()
    view = views.DocumentCreateView()
    view.setup(request)
    response = view.form_valid(form)
    assert response.url == reverse('documents:home')


def test_documents_edit_view_get_document_form_returns_form(
    db, document_collection_fixture
):
    obj = document_collection_fixture()[0]
    request = RequestFactory().get(reverse('documents:edit', kwargs={'slug': obj.slug}))
    view = views.DocumentEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    form = view.get_form()
    assert isinstance(form, DocumentCollectionForm)


def test_documents_edit_view_context_data_is_dict(db, document_collection_fixture):
    obj = document_collection_fixture()[0]
    request = RequestFactory().get(reverse('documents:edit', kwargs={'slug': obj.slug}))
    view = views.DocumentEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)


def test_documents_edit_view_form_valid_redirects_to_documents_home(
    db, document_collection_fixture, document_collection_form_fixture
):
    obj = document_collection_fixture()[0]
    c = Client()
    user = UserFactory()
    request = c.get(reverse('documents:edit', kwargs={'slug': obj.slug})).wsgi_request
    request.user = user
    form = document_collection_form_fixture()
    view = views.DocumentEditView()
    view.setup(request)
    response = view.form_valid(form)
    assert response.url == reverse('documents:home')


def test_documents_delete_get_method_shows_error_if_user_not_owner(db):
    user1 = UserFactory()
    user2 = UserFactory()
    obj = CollectionArchiveFactory(administrator=user1)
    c = Client()
    request = c.get(reverse('documents:delete', kwargs={'slug': obj.slug})).wsgi_request
    request.user = user2
    view = views.DocumentDeleteView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    view.get(request)
    messages = list(get_messages(request))
    assert messages[0].level_tag == 'message-error'


def test_documents_delete_get_method_deletes_object_if_user_is_owner(db):
    user1 = UserFactory()
    obj = CollectionArchiveFactory(administrator=user1)
    c = Client()
    request = c.get(reverse('documents:delete', kwargs={'slug': obj.slug})).wsgi_request
    request.user = user1
    view = views.DocumentDeleteView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    response = view.get(request)
    assert response.url == reverse('documents:home')

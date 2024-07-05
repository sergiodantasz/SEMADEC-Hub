from django.contrib.messages import get_messages
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.test import Client, RequestFactory
from django.urls import resolve, reverse
from pytest import raises as assert_raises

from apps.archive import views
from apps.archive.forms import ImageForm
from apps.competitions.forms import SportForm
from apps.users.tests.factories import UserFactory


def test_archive_list_view_get_queryset_method_returns_queryset():
    view = views.ArchiveListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_archive_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('archive:home'))
    request.resolver_match = resolve(reverse('archive:home'))
    response = views.ArchiveListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_archive_search_view_get_queryset_method_returns_queryset(db):
    request = RequestFactory().get(reverse('archive:search'))
    request.GET |= {'q': 'test'}
    view = views.ArchiveSearchView()
    view.setup(request)
    queryset = view.get_queryset()
    assert isinstance(queryset, QuerySet)


def test_archive_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('archive:search'))
    request.GET |= {'q': 'test'}
    response = views.ArchiveSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_archive_create_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('archive:create'))
    request.resolver_match = resolve(reverse('archive:create'))
    request.user = UserFactory(is_admin=True)
    response = views.ArchiveCreateView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_archive_create_view_get_image_form_returns_form():
    request = RequestFactory().get(reverse('archive:create'))
    view = views.ArchiveCreateView()
    view.setup(request)
    form = view.get_image_form()
    assert isinstance(form, ImageForm)


def test_archive_create_view_form_valid_redirects_to_archive_home(
    db, collection_archive_fixture
):
    c = Client()
    user = UserFactory()
    request = c.get(reverse('archive:create')).wsgi_request
    request.user = user
    form = collection_archive_fixture()
    view = views.ArchiveCreateView()
    view.setup(request)
    response = view.form_valid(form)
    assert response.url == reverse('archive:home')


def test_archive_edit_view_context_data_is_dict(db, collection_archive_fixture):
    obj = collection_archive_fixture()
    c = Client()
    request = c.get(reverse('archive:edit', kwargs={'slug': obj.slug})).wsgi_request
    request.user = UserFactory(is_admin=True)
    view = views.ArchiveEditView()
    view.setup(request, slug=obj.slug)
    response = view.get(request)
    assert isinstance(response.context_data, dict)


def test_archive_edit_view_get_image_form_returns_form(db, collection_archive_fixture):
    obj = collection_archive_fixture()
    request = RequestFactory().get(reverse('archive:edit', kwargs={'slug': obj.slug}))
    view = views.ArchiveEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    form = view.get_image_form()
    assert isinstance(form, ImageForm)


def test_archive_edit_view_form_valid_redirects_to_archive_home(
    db, collection_archive_fixture
):
    obj = collection_archive_fixture()
    c = Client()
    user = UserFactory()
    request = c.get(reverse('archive:edit', kwargs={'slug': obj.slug})).wsgi_request
    request.user = user
    form = collection_archive_fixture()
    view = views.ArchiveEditView()
    view.setup(request, slug=obj.slug)
    response = view.form_valid(form)
    assert response.url == reverse('archive:home')


def test_archive_detail_view_context_data_is_dict(db, collection_archive_fixture):
    obj = collection_archive_fixture()
    user = UserFactory(is_admin=True)
    request = RequestFactory().get(reverse('archive:detail', kwargs={'slug': obj.slug}))
    request.user = user
    view = views.ArchiveDetailView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)


def test_archive_image_delete_view_get_method_redirects_to_archive_home(
    db, image_fixture
):
    user = UserFactory()
    obj = image_fixture(collection__administrator=user)[0]
    c = Client()
    request = c.get(reverse('archive:image:delete', kwargs={'pk': obj.pk})).wsgi_request
    request.user = user
    view = views.ArchiveImageDeleteView()
    view.setup(request, pk=obj.pk)
    view.get(request)
    assert list(get_messages(request))[0].level_tag == 'message-success'


def test_archive_image_delete_view_get_method_raises_permissionerror_if_user_is_not_owner(
    db, image_fixture
):
    user = UserFactory()
    user2 = UserFactory()
    obj = image_fixture(collection__administrator=user)[0]
    c = Client()
    request = c.get(reverse('archive:image:delete', kwargs={'pk': obj.pk})).wsgi_request
    request.user = user2
    view = views.ArchiveImageDeleteView()
    view.setup(request, pk=obj.pk)
    with assert_raises(PermissionDenied):
        view.get(request)

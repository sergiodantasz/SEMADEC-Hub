from django.db.models.query import QuerySet
from django.test import RequestFactory
from django.urls import resolve, reverse

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


def test_archive_create_view_get__image_form_returns_form():
    request = RequestFactory().get(reverse('archive:create'))
    view = views.ArchiveCreateView()
    view.setup(request)
    form = view.get_image_form()
    assert isinstance(form, ImageForm)


def test_archive_edit_view_get_image_form_returns_form(db, collection_archive_fixture):
    obj = collection_archive_fixture()
    request = RequestFactory().get(reverse('archive:edit', kwargs={'slug': obj.slug}))
    view = views.ArchiveEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    form = view.get_image_form()
    assert isinstance(form, ImageForm)


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

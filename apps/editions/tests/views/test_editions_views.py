import django
from django.conf import settings
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.db.models.query import QuerySet
from django.test import Client, RequestFactory
from django.urls import resolve, reverse

from apps.competitions.tests.factories import SportFactory
from apps.editions import views
from apps.editions.forms import EditionForm, EditionTeamForm
from apps.teams.tests.factories import TeamFactory
from apps.users.tests.factories import UserFactory

django.setup()


def test_edition_list_view_get_queryset_method_returns_queryset():
    view = views.EditionListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_edition_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('editions:home'))
    request.resolver_match = resolve(reverse('editions:home'))
    response = views.EditionListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_edition_detail_view_context_data_is_dict(db, edition_fixture):
    obj = edition_fixture()
    request = RequestFactory().get(reverse('editions:detailed', kwargs={'pk': obj.pk}))
    view = views.EditionDetailView()
    view.setup(request, pk=obj.pk)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)


def test_edition_search_view_get_queryset_method_returns_queryset(db):
    request = RequestFactory().get(reverse('editions:search'))
    request.GET |= {'q': 'test'}
    view = views.EditionSearchView()
    view.setup(request)
    queryset = view.get_queryset()
    assert isinstance(queryset, QuerySet)


def test_edition_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('editions:search'))
    request.GET |= {'q': 'test'}
    response = views.EditionSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_edition_create_view_context_data_is_dict(db):
    SportFactory()
    TeamFactory()
    request = RequestFactory().get(reverse('editions:create'))
    request.resolver_match = resolve(reverse('editions:create'))
    request.user = UserFactory(is_admin=True)
    response = views.EditionCreateView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_edition_create_view_get_raises_error_if_no_team(db):
    SportFactory()
    c = Client()
    request = c.get(reverse('editions:create')).wsgi_request
    view = views.EditionCreateView()
    view.setup(request)
    view.get(request)
    messages = list(get_messages(request))
    assert len(messages) == 1


def test_edition_create_view_get_raises_error_if_no_sport(db):
    TeamFactory()
    c = Client()
    request = c.get(reverse('editions:create')).wsgi_request
    view = views.EditionCreateView()
    view.setup(request)
    view.get(request)
    messages = list(get_messages(request))
    assert len(messages) == 1


def test_edition_create_view_get_renders_response_if_no_errors(db):
    SportFactory()
    TeamFactory()
    c = Client()
    request = c.get(reverse('editions:create')).wsgi_request
    view = views.EditionCreateView()
    view.setup(request)
    response = view.get(request)
    assert response._request.path == reverse('editions:create')


def test_edition_edit_view_context_data_is_dict(db, edition_fixture):
    obj = edition_fixture()
    request = RequestFactory().get(reverse('editions:edit', kwargs={'pk': obj.pk}))
    view = views.EditionEditView()
    view.setup(request, pk=obj.pk)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)


def test_edition_edit_view_get_form_returns_form(db, edition_fixture):
    obj = edition_fixture()
    request = RequestFactory().get(reverse('editions:edit', kwargs={'pk': obj.pk}))
    view = views.EditionEditView()
    view.setup(request, pk=obj.pk)
    view.object = obj
    form = view.get_form()
    assert isinstance(form, EditionForm)


def test_edition_edit_view_get_form_teams_returns_form(db, edition_fixture):
    obj = edition_fixture()
    request = RequestFactory().get(reverse('editions:edit', kwargs={'pk': obj.pk}))
    view = views.EditionEditView()
    view.setup(request, pk=obj.pk)
    view.object = obj
    form = view.get_form_teams()
    assert isinstance(form.empty_form, EditionTeamForm)


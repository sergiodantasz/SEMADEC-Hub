from django.contrib.messages import get_messages
from django.db.models.query import QuerySet
from django.test import Client, RequestFactory
from django.urls import resolve, reverse

from apps.competitions import views
from apps.competitions.forms import MatchForm
from apps.editions.tests.factories import EditionFactory
from apps.teams.tests.factories import TeamFactory
from apps.users.tests.factories import UserFactory


def test_match_create_view_context_data_is_dict(db):
    edition_obj = EditionFactory()
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:create', kwargs={'pk': edition_obj.pk})
    ).wsgi_request
    request.user = UserFactory(is_admin=True)
    view = views.MatchCreateView()
    view.setup(request, pk=edition_obj.pk)
    response = view.get_context_data()
    assert isinstance(response, dict)


def test_match_create_view_get_success_url_returns_correct_url(db):
    edition_obj = EditionFactory()
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:create', kwargs={'pk': edition_obj.pk})
    ).wsgi_request
    request.user = UserFactory(is_admin=True)
    view = views.MatchCreateView()
    view.setup(request, pk=edition_obj.pk)
    response = view.get_success_url()
    assert response == reverse('editions:detailed', kwargs={'pk': edition_obj.pk})


def test_match_create_view_get_form_returns_form(db):
    edition_obj = EditionFactory()
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:create', kwargs={'pk': edition_obj.pk})
    ).wsgi_request
    request.user = UserFactory(is_admin=True)
    view = views.MatchCreateView()
    view.setup(request, pk=edition_obj.pk)
    response = view.get_form()
    assert isinstance(response, MatchForm)


def test_match_create_view_get_raises_error_if_no_team(db):
    edition_obj = EditionFactory()
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:create', kwargs={'pk': edition_obj.pk})
    ).wsgi_request
    view = views.MatchCreateView()
    view.setup(request, pk=edition_obj.pk)
    view.get(request)
    messages = list(get_messages(request))
    assert messages[0].level_tag == 'message-error'


def test_match_create_view_get_renders_response_if_no_errors(db):
    TeamFactory()
    edition_obj = EditionFactory()
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:create', kwargs={'pk': edition_obj.pk})
    ).wsgi_request
    view = views.MatchCreateView()
    view.setup(request, pk=edition_obj.pk)
    response = view.get(request)
    assert response._request.path == reverse(
        'competitions:sports:matches:create', kwargs={'pk': edition_obj.pk}
    )


def test_match_create_view_form_valid_redirects_to_matches_home(db, match_form_fixture):
    edition_obj = EditionFactory()
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:create', kwargs={'pk': edition_obj.pk})
    ).wsgi_request
    view = views.MatchCreateView()
    view.setup(request, pk=edition_obj.pk)
    form = match_form_fixture()
    response = view.form_valid(form)
    assert response.url == reverse('editions:detailed', kwargs={'pk': edition_obj.pk})


def test_match_edit_view_context_data_is_dict(db, match_fixture, match_form_fixture):
    obj = match_fixture()
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:edit', kwargs={'pk': obj.pk})
    ).wsgi_request
    request.user = UserFactory(is_admin=True)
    view = views.MatchEditView()
    view.setup(request, pk=obj.pk)
    response = view.get(request)
    assert isinstance(response.context_data, dict)


def test_match_edit_view_get_success_url_returns_correct_url(db, match_fixture):
    obj = match_fixture()
    edition_pk = obj.edition.pk
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:edit', kwargs={'pk': obj.pk})
    ).wsgi_request
    request.user = UserFactory(is_admin=True)
    view = views.MatchEditView()
    view.setup(request, pk=obj.pk)
    response = view.get_success_url()
    assert response == reverse('editions:detailed', kwargs={'pk': edition_pk})


def test_match_edit_view_get_form_returns_form(db, match_fixture, match_form_fixture):
    obj = match_fixture()
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:edit', kwargs={'pk': obj.pk})
    ).wsgi_request
    request.user = UserFactory(is_admin=True)
    view = views.MatchEditView()
    view.setup(request, pk=obj.pk)
    form = match_form_fixture()
    response = view.get_form(form)
    assert isinstance(response, MatchForm)


def test_match_delete_view_get_success_url_returns_correct_url(db, match_fixture):
    obj = match_fixture()
    edition_pk = obj.edition.pk
    c = Client()
    request = c.get(
        reverse('competitions:sports:matches:delete', kwargs={'pk': obj.pk})
    ).wsgi_request
    request.user = UserFactory(is_admin=True)
    view = views.MatchDeleteView()
    view.setup(request, pk=obj.pk)
    response = view.get_success_url()
    assert response == reverse('editions:detailed', kwargs={'pk': edition_pk})

from django.contrib.messages import get_messages
from django.db.models.query import QuerySet
from django.test import Client, RequestFactory
from django.urls import resolve, reverse

from apps.competitions import views
from apps.competitions.forms import SportForm, TestForm, TestTeamForm
from apps.teams.tests.factories import TeamFactory
from apps.users.tests.factories import UserFactory


def test_test_list_view_get_queryset_method_returns_queryset():
    view = views.TestListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_test_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('competitions:tests:home'))
    request.resolver_match = resolve(reverse('competitions:tests:home'))
    response = views.TestListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_test_search_view_get_queryset_method_returns_queryset(db):
    request = RequestFactory().get(reverse('competitions:tests:search'))
    request.GET |= {'q': 'test'}
    view = views.TestSearchView()
    view.setup(request)
    queryset = view.get_queryset()
    assert isinstance(queryset, QuerySet)


def test_test_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('competitions:tests:search'))
    request.GET |= {'q': 'test'}
    response = views.TestSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_test_create_view_context_data_is_dict(db):
    TeamFactory()
    request = RequestFactory().get(reverse('competitions:tests:create'))
    request.resolver_match = resolve(reverse('competitions:tests:create'))
    request.user = UserFactory(is_admin=True)
    response = views.TestCreateView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_test_create_view_get_raises_error_if_no_team(db):
    c = Client()
    request = c.get(reverse('competitions:tests:create')).wsgi_request
    view = views.TestCreateView()
    view.setup(request)
    view.get(request)
    messages = list(get_messages(request))
    assert messages[0].level_tag == 'message-error'


def test_test_create_view_get_renders_response_if_no_errors(db):
    TeamFactory()
    c = Client()
    request = c.get(reverse('competitions:tests:create')).wsgi_request
    view = views.TestCreateView()
    view.setup(request)
    response = view.get(request)
    assert response._request.path == reverse('competitions:tests:create')


def test_tests_edit_view_context_data_is_dict(db, test_fixture):
    obj = test_fixture()
    request = RequestFactory().get(
        reverse('competitions:tests:edit', kwargs={'slug': obj.slug})
    )
    view = views.TestEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)


def test_test_edit_view_get_form_returns_form(db, test_fixture):
    obj = test_fixture()
    request = RequestFactory().get(
        reverse('competitions:tests:edit', kwargs={'slug': obj.slug})
    )
    view = views.TestEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    form = view.get_form()
    assert isinstance(form, TestForm)


def test_test_edit_view_get_form_teams_returns_form(db, test_fixture):
    obj = test_fixture()
    request = RequestFactory().get(
        reverse('competitions:tests:edit', kwargs={'slug': obj.slug})
    )
    view = views.TestEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    form = view.get_form_teams()
    assert isinstance(form.empty_form, TestTeamForm)


def test_test_create_post_method_redirects_to_correct_url(db, test_fixture):
    obj = test_fixture()
    c = Client()
    request = c.get(
        reverse('competitions:tests:edit', kwargs={'slug': obj.slug})
    ).wsgi_request
    view = views.TestEditView()
    view.setup(request, slug=obj.slug)
    response = view.post(request)
    assert response.url == reverse('competitions:tests:home')


def test_test_detail_view_context_data_is_dict(db, test_fixture):
    obj = test_fixture()
    request = RequestFactory().get(
        reverse('competitions:tests:detailed', kwargs={'slug': obj.slug})
    )
    view = views.TestDetailView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)

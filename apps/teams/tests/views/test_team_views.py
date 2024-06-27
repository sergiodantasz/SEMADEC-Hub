from django.db.models.query import QuerySet
from django.test import RequestFactory
from django.urls import resolve, reverse

from apps.teams.tests.factories import ClassFactory
from apps.teams.views import views_teams as views
from apps.users.tests.factories import UserFactory


def test_team_list_view_get_queryset_method_returns_queryset():
    view = views.TeamListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_team_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:home'))
    request.resolver_match = resolve(reverse('teams:home'))
    response = views.TeamListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_team_search_view_get_queryset_method_returns_queryset(db):
    request = RequestFactory().get(reverse('teams:search'))
    request.GET |= {'q': 'test'}
    view = views.TeamSearchView()
    view.setup(request)
    queryset = view.get_queryset()
    assert isinstance(queryset, QuerySet)


def test_team_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:search'))
    request.GET |= {'q': 'test'}
    response = views.TeamSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_team_create_view_context_data_is_dict(db):
    ClassFactory()
    request = RequestFactory().get(reverse('teams:create'))
    request.resolver_match = resolve(reverse('teams:create'))
    request.user = UserFactory(is_admin=True)
    response = views.TeamCreateView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_team_edit_view_context_data_is_dict(db, team_fixture):
    obj = team_fixture()
    request = RequestFactory().get(reverse('teams:edit', kwargs={'slug': obj.slug}))
    view = views.TeamEditView()
    view.setup(request, slug=obj.pk)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)

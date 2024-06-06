from django.urls import resolve, reverse

from apps.teams.views import views_teams as views


def test_teams_home_viewname_redirects_to_teams_list_view():
    view = resolve(reverse('teams:home'))
    assert view.func.view_class is views.TeamListView


def test_teams_search_viewname_redirects_to_teams_search_view():
    view = resolve(reverse('teams:search'))
    assert view.func.view_class is views.TeamSearchView


def test_teams_create_viewname_redirects_to_teams_create_view():
    view = resolve(reverse('teams:create'))
    assert view.func.view_class is views.TeamCreateView


def test_teams_edit_viewname_redirects_to_teams_edit_view():
    view = resolve(reverse('teams:edit', kwargs={'slug': 'test'}))
    assert view.func.view_class is views.TeamEditView


def test_teams_delete_viewname_redirects_to_teams_Delete_view():
    view = resolve(reverse('teams:delete', kwargs={'slug': 'test'}))
    assert view.func.view_class is views.TeamDeleteView

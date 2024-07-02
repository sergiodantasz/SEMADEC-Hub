from django.urls import resolve, reverse

from apps.competitions import views


def test_matches_create_viewname_redirects_to_matches_create_view():
    view = resolve(reverse('competitions:sports:matches:create', kwargs={'pk': 1}))
    assert view.func.view_class is views.MatchCreateView


def test_matches_edit_viewname_redirects_to_matches_edit_view():
    view = resolve(reverse('competitions:sports:matches:edit', kwargs={'pk': 1}))
    assert view.func.view_class is views.MatchEditView

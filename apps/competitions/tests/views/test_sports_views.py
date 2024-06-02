from django.urls import resolve, reverse

from apps.competitions import views


def test_sports_viewname_redirects_to_sports_view():
    view = resolve(reverse('competitions:sports:home'))
    assert view.func.view_class is views.SportView


def test_sports_detailed_viewname_redirects_to_sports_detailed_view():
    view = resolve(reverse('competitions:sports:detailed', kwargs={'slug': 'test'}))
    assert view.func.view_class is views.SportDetailedView


def test_sports_create_viewname_redirects_to_sports_create_view():
    view = resolve(reverse('competitions:sports:create'))
    assert view.func.view_class is views.SportCreateView


def test_sports_search_viewname_redirects_to_sports_search_view():
    view = resolve(reverse('competitions:sports:search'))
    assert view.func.view_class is views.SportSearchView


def test_sports_edit_viewname_redirects_to_sports_edit_view():
    view = resolve(reverse('competitions:sports:edit', kwargs={'slug': 'test'}))
    assert view.func.view_class is views.SportEditView


def test_sports_delete_viewname_redirects_to_sports_delete_view():
    view = resolve(reverse('competitions:sports:delete', kwargs={'slug': 'test'}))
    assert view.func.view_class is views.SportDeleteView

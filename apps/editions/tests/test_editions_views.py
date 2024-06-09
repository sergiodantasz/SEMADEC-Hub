from django.urls import resolve, reverse

from apps.editions import views


def test_editions_viewname_redirects_to_editions_view():
    view = resolve(reverse('editions:home'))
    assert view.func.view_class is views.EditionListView


def test_editions_create_viewname_redirects_to_editions_create_view():
    view = resolve(reverse('editions:create'))
    assert view.func.view_class is views.EditionCreateView


def test_editions_search_viewname_redirects_to_editions_search_view():
    view = resolve(reverse('editions:search'))
    assert view.func.view_class is views.EditionSearchView


def test_editions_detailed_viewname_redirects_to_editions_detailed_view():
    view = resolve(reverse('editions:detailed', kwargs={'pk': 1}))
    assert view.func.view_class is views.EditionDetailView


def test_editions_edit_viewname_redirects_to_editions_edit_view():
    view = resolve(reverse('editions:edit', kwargs={'pk': 1}))
    assert view.func.view_class is views.EditionEditView


def test_editions_delete_viewname_redirects_to_editions_delete_view():
    view = resolve(reverse('editions:delete', kwargs={'pk': 1}))
    assert view.func.view_class is views.EditionDeleteView

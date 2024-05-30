from django.urls import resolve, reverse

from apps.competitions import views


def test_tests_viewname_redirects_to_tests_view():
    view = resolve(reverse('competitions:tests:home'))
    assert view.func is views.tests


def test_tests_detailed_viewname_redirects_to_tests_detailed_view():
    view = resolve(reverse('competitions:tests:detailed', kwargs={'slug': 'test'}))
    assert view.func is views.tests_detailed


def test_tests_create_viewname_redirects_to_tests_create_view():
    view = resolve(reverse('competitions:tests:create'))
    assert view.func is views.tests_create


def test_tests_search_viewname_redirects_to_tests_search_view():
    view = resolve(reverse('competitions:tests:search'))
    assert view.func is views.tests_search


def test_tests_edit_viewname_redirects_to_tests_edit_view():
    view = resolve(reverse('competitions:tests:edit', kwargs={'slug': 'test'}))
    assert view.func is views.tests_edit


def test_tests_delete_viewname_redirects_to_tests_delete_view():
    view = resolve(reverse('competitions:tests:delete', kwargs={'slug': 'test'}))
    assert view.func is views.tests_delete

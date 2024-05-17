from django.urls import resolve, reverse

from competitions import views


def test_competitions_viewname_redirects_to_sports_view():
    view = resolve(reverse('competitions:home'))
    assert view.func is views.competitions


def test_sports_viewname_redirects_to_sports_view():
    view = resolve(reverse('competitions:sports:home'))
    assert view.func is views.sports


def test_sports_search_viewname_redirects_to_sports_search_view():
    view = resolve(reverse('competitions:sports:search'))
    assert view.func is views.sports_search


def test_tests_viewname_redirects_to_tests_view():
    view = resolve(reverse('competitions:tests:home'))
    assert view.func is views.tests


def test_tests_search_viewname_redirects_to_tests_search_view():
    view = resolve(reverse('competitions:tests:search'))
    assert view.func is views.tests_search

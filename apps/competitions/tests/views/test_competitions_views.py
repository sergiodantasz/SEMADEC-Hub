from django.urls import resolve, reverse

from apps.competitions import views


def test_competitions_viewname_redirects_to_sports_view():
    view = resolve(reverse('competitions:home'))
    assert view.func is views.competitions

from django.test import RequestFactory
from django.urls import resolve, reverse

from apps.competitions import views


def test_competitions_viewname_redirects_to_sports_view():
    view = resolve(reverse('competitions:home'))
    assert view.func.view_class is views.CompetitionView


def test_competitions_view_redirects_to_sports_view():
    request = RequestFactory().get('/competitions/')
    response = views.CompetitionView.as_view()(request)
    assert response.url == reverse('competitions:sports:home')

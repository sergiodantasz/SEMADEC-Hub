from django.urls import resolve, reverse

from apps.home import views


def test_home_viewname_redirects_to_home_view():
    view = resolve(reverse('home:home'))
    assert view.func.view_class is views.HomeView

from django.urls import resolve, reverse

from editions import views


def test_editions_viewname_redirects_to_editions_view():
    view = resolve(reverse('editions:editions'))
    assert view.func is views.editions

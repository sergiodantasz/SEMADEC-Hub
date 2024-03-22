from django.urls import resolve, reverse

from users import views


def test_profile_viewname_redirects_to_profile_view():
    view = resolve(reverse('users:profile'))
    assert view.func is views.profile


def test_login_viewname_redirects_to_login_view():
    view = resolve(reverse('users:login'))
    assert view.func is views.login


def test_logout_viewname_redirects_to_logout_view():
    view = resolve(reverse('users:logout'))
    assert view.func is views.logout

from django.urls import resolve, reverse

from apps.users import views


def test_profile_viewname_redirects_to_profile_view():
    view = resolve(reverse('users:profile'))
    assert view.func.view_class is views.ProfileView


def test_login_viewname_redirects_to_login_view():
    view = resolve(reverse('users:login'))
    assert view.func.view_class is views.LoginView


def test_logout_viewname_redirects_to_logout_view():
    view = resolve(reverse('users:logout'))
    assert view.func.view_class is views.LogoutView

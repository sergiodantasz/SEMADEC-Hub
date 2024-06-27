from django.contrib.auth.models import AnonymousUser
from django.db.models.query import QuerySet
from django.test import RequestFactory
from django.urls import resolve, reverse

from apps.competitions.forms import SportForm
from apps.users import views
from apps.users.tests.factories import UserFactory


def test_login_view_redirects_to_profile_view_if_user_is_authenticated(
    db, user_fixture
):
    request = RequestFactory().get(reverse('users:login'))
    request.resolver_match = resolve(reverse('users:login'))
    request.user = user_fixture()
    response = views.LoginView.as_view()(request)
    assert response.url == reverse('users:profile')


def test_login_view_redirects_to_suap_view_if_user_is_not_authenticated(db):
    request = RequestFactory().get(reverse('users:login'))
    request.resolver_match = resolve(reverse('users:login'))
    request.user = AnonymousUser()
    response = views.LoginView.as_view()(request)
    assert response.url == reverse('social:begin', kwargs={'backend': 'suap'})


def test_profile_view_context_data_is_dict(db, user_fixture):
    request = RequestFactory().get(reverse('users:profile'))
    request.resolver_match = resolve(reverse('users:profile'))
    request.user = user_fixture()
    response = views.ProfileView.as_view()(request)
    assert isinstance(response.context_data, dict)

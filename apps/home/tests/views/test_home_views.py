from django.db.models.query import QuerySet
from django.test import RequestFactory
from django.urls import resolve, reverse

from apps.home import views
from apps.users.tests.factories import UserFactory


def test_home_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('home:home'))
    request.resolver_match = resolve(reverse('home:home'))
    response = views.HomeView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_tag_list_view_get_queryset_method_returns_queryset():
    view = views.TagListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_tag_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('home:tags:home'))
    request.resolver_match = resolve(reverse('home:tags:home'))
    response = views.TagListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_tag_create_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('home:tags:create'))
    request.resolver_match = resolve(reverse('home:tags:create'))
    request.user = UserFactory(is_admin=True)
    response = views.TagCreateView.as_view()(request)
    assert isinstance(response.context_data, dict)

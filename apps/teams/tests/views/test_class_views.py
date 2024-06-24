from django.db.models.query import QuerySet
from django.test import RequestFactory
from django.urls import resolve, reverse

from apps.teams.views import views_classes as views


def test_class_list_view_get_queryset_method_returns_queryset():
    view = views.ClassListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_class_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:classes:home'))
    request.resolver_match = resolve(reverse('teams:classes:home'))
    response = views.ClassListView.as_view()(request)
    assert isinstance(response.context_data, dict)

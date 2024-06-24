from django.db.models.query import QuerySet
from django.test import RequestFactory
from django.urls import resolve, reverse
from pytest import mark

from apps.teams.views import views_courses as views


def test_course_list_view_get_queryset_method_returns_queryset():
    view = views.CourseListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_course_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:courses:home'))
    request.resolver_match = resolve(reverse('teams:courses:home'))
    response = views.CourseListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_course_search_view_get_queryset_method_returns_queryset(db):
    request = RequestFactory().get(reverse('teams:courses:search'))
    request.GET |= {'q': 'test'}
    view = views.CourseSearchView()
    view.request = request
    assert isinstance(view.get_queryset(), QuerySet)


def test_course_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:courses:search'))
    request.GET |= {'q': 'test'}
    response = views.CourseSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)

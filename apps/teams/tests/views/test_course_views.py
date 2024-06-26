from django.db.models.query import QuerySet
from django.test import RequestFactory
from django.urls import resolve, reverse

from apps.teams.views import views_courses as views
from apps.users.tests.factories import UserFactory


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
    view.setup(request)
    queryset = view.get_queryset()
    assert isinstance(queryset, QuerySet)


def test_course_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:courses:search'))
    request.GET |= {'q': 'test'}
    response = views.CourseSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_course_create_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:courses:create'))
    request.resolver_match = resolve(reverse('teams:courses:create'))
    request.user = UserFactory(is_admin=True)
    response = views.CourseCreateView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_course_edit_view_context_data_is_dict(db, course_fixture):
    obj = course_fixture(slug='test-slug')
    request = RequestFactory().post(
        reverse('teams:courses:edit', kwargs={'slug': 'test-slug'})
    )
    view = views.CourseEditView()
    view.setup(request)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)

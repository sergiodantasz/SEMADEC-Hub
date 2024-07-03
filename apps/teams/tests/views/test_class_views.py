from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.db.models.query import QuerySet
from django.http import QueryDict
from django.test import Client, RequestFactory
from django.urls import resolve, reverse
from pytest import mark

from apps.teams.models import Course
from apps.teams.views import views_classes as views
from apps.users.tests.factories import UserFactory


def test_class_list_view_get_queryset_method_returns_queryset():
    view = views.ClassListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_class_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:classes:home'))
    request.resolver_match = resolve(reverse('teams:classes:home'))
    response = views.ClassListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_class_search_view_get_queryset_method_returns_queryset(db):
    request = RequestFactory().get(reverse('teams:classes:search'))
    request.GET |= {'q': 'test'}
    view = views.ClassSearchView()
    view.request = request
    assert isinstance(view.get_queryset(), QuerySet)


def test_class_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:classes:search'))
    request.GET |= {'q': 'test'}
    response = views.ClassSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_class_create_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('teams:classes:create'))
    view = views.ClassCreateView()
    view.setup(request)
    context = view.get_context_data()
    assert isinstance(context, dict)


def test_class_create_get_method_shows_error_if_no_course_found(db):
    c = Client()
    request = c.get(reverse('teams:classes:create')).wsgi_request
    view = views.ClassCreateView()
    view.setup(request)
    view.get(request)
    messages = list(get_messages(request))
    assert messages[0].level_tag == 'message-error'


def test_class_create_get_method(db, course_fixture):
    course_fixture()
    c = Client()
    request = c.get(reverse('teams:classes:create')).wsgi_request
    view = views.ClassCreateView()
    view.setup(request)
    response = view.get(request)
    assert response._request.path == reverse('teams:classes:create')


def test_class_edit_view_context_data_is_dict(db, class_fixture):
    obj = class_fixture(slug='test-slug')
    request = RequestFactory().get(
        reverse('teams:classes:edit', kwargs={'slug': 'test-slug'})
    )
    view = views.ClassEditView()
    view.setup(request)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)

from django.contrib.messages import get_messages
from django.db.models import Q
from django.http import QueryDict
from django.test import Client, RequestFactory
from django.urls import resolve, reverse
from pytest import mark

from apps.teams.models import Course
from apps.teams.tests.factories import CourseFactory
from base.views import BaseSearchView, MessageMixin
from base.views.base_form_views import BaseDeleteView


def test_message_mixin_is_model_populated_adds_success_message_if_success_message(
    db,
):
    c = Client()
    success_message = 'Test success message'
    obj = MessageMixin()
    obj.request = c.get('/').wsgi_request
    obj.success_message = success_message
    obj.is_model_populated(Course)
    assert list(get_messages(obj.request))[0].message == success_message


def test_message_mixin_is_model_populated_adds_error_message_if_success_error_message(
    db,
):
    c = Client()
    error_message = 'Test error message'
    obj = MessageMixin()
    obj.request = c.get('/').wsgi_request
    obj.error_message = error_message
    obj.is_model_populated(Course)
    assert list(get_messages(obj.request))[0].message == error_message


def test_base_search_view_raises_error_if_querystr_is_empty(db):
    c = Client()
    response = c.get('/')
    request = response._request
    setattr(request, 'GET', QueryDict(mutable=True))
    request.GET['q'] = ''
    view = BaseSearchView()
    view.setup(request)
    view.model = Course
    view.get_queryset(Q(), 'name')
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1


def test_base_search_view_does_not_raise_error_if_querystr_is_not_empty(db):
    c = Client()
    response = c.get('/')
    request = response._request
    setattr(request, 'GET', QueryDict(mutable=True))
    request.GET['q'] = 'test'
    view = BaseSearchView()
    view.setup(request)
    view.model = Course
    view.get_queryset(Q(), 'name')
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 0


def test_base_delete_view_get_method_redirects_to_success_url(db):
    obj = CourseFactory.create_batch(1)[0]
    obj.save()
    request = RequestFactory().get(
        reverse('teams:courses:delete', kwargs={'slug': obj.slug})
    )
    request.resolver_match = resolve(
        reverse('teams:courses:delete', kwargs={'slug': obj.slug})
    )
    view = BaseDeleteView()
    view.model = Course
    view.setup(request, slug=obj.slug)
    response = view.get(request, slug=obj.slug)
    assert response.url == view.get_success_url()

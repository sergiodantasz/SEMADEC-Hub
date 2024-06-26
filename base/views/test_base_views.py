from django.contrib.messages import get_messages
from django.db.models import Q
from django.http import QueryDict
from django.test import Client

from apps.teams.models import Course
from base.views import BaseSearchView


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

from django.http import Http404
from django.test import RequestFactory
from django.urls import resolve
from pytest import mark

from apps.handlers import views


@mark.skip
def test_handler_view_page_not_found_404_loads_correct_view():
    request = RequestFactory().get('/')
    view = views.page_not_found_404(request, Http404)
    ...

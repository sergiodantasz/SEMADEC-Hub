from django.core.exceptions import BadRequest, PermissionDenied
from django.http import Http404
from django.test import RequestFactory
from django.urls import resolve
from pytest import mark

from apps.handlers import views


def test_handler_view_page_not_found_404_loads_correct_view():
    request = RequestFactory().get('/')
    view = views.page_not_found_404(request, Http404)
    assert view.status_code == 404


def test_handler_view_page_server_error_500_loads_correct_view():
    request = RequestFactory().get('/')
    view = views.server_error_500(request)
    assert view.status_code == 500


def test_handler_view_page_permission_denied_403_loads_correct_view():
    request = RequestFactory().get('/')
    view = views.permission_denied_403(request, PermissionDenied)
    assert view.status_code == 403


def test_handler_view_page_bad_request_400_loads_correct_view():
    request = RequestFactory().get('/')
    view = views.bad_request_400(request, BadRequest)
    assert view.status_code == 400

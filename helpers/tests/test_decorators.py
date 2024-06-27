from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory
from pytest import raises as assert_raises

from apps.users.tests.factories import UserFactory
from helpers.decorators import admin_required


@admin_required
def dummy_view(request, *args, **kwargs):
    return HttpResponse()


def test_admin_required_raise_permissiondenied_if_user_is_not_admin(db):
    request = RequestFactory().get('/')
    request.user = UserFactory(is_admin=False)
    with assert_raises(PermissionDenied):
        dummy_view(request)


def test_admin_required_return_function_if_user_is_admin(db):
    request = RequestFactory().get('/')
    request.user = UserFactory(is_admin=True)
    response = dummy_view(request)
    assert isinstance(response, HttpResponse)

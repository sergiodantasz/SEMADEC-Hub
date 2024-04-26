from django.forms import CharField

from helpers import form


def test_forms_helpers_set_attr_function_returns_none():
    call = form.set_attr(CharField(), 'name', 'value')
    assert call is None


def test_forms_helpers_set_placeholder_function_returns_none():
    call = form.set_placeholder(CharField(), 'value')
    assert call is None

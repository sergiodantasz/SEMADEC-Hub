from os import path
from typing import Any

from django import template
from django.db.models import QuerySet
from django.forms.boundfield import BoundField
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.users.models import User

register = template.Library()


@register.simple_tag()
def load_regs(
    db_regs: QuerySet,
    template: str,
    empty: str,
    user=None,
    reg: str = 'reg',
    div: str = '',
):
    """Load regs inside a Django QuerySet of returns error message if none exists.

    Args:
        db_regs (QuerySet): QuerySet object related to model query.
        template (str): Template name to be used.
        empty (str): Message to display if the given QuerySet is empty.
        user (User, optional): Object representing the user that made the request.
        reg (str, optional): Object variable name to be used during iteration.
        div (str, optional): Div class name for objects wrapping.

    Returns:
        SafeString: Output string to be appended on html page.
    """
    if db_regs:
        process = (render_to_string(template, {reg: i, 'user': user}) for i in db_regs)
        final_content = ''.join(process)
        if div:
            container = '<div class={}>{}</div>'
            container = container.format(div, final_content)
            return mark_safe(container)
        return mark_safe(final_content)
    else:
        return mark_safe(f'<p class="nothing-found">{empty}</p>')


@register.simple_tag()
def check_error(field: BoundField):
    """Check errors inside a form field
    Args:
        field (BoundField): BoundField object that represents the form field
    Returns:
        SafeString | str: Empty string or containing HTML error containers
    """
    if field.errors:
        container_outer = '<div class="field-errors">{}</div>'
        errors_list = []
        for error in field.errors:
            container_inner = f'<div class="field-error">{error}</div>'
            errors_list.append(container_inner)
        final_content = ''.join(errors_list)
        container_outer = container_outer.format(final_content)
        return mark_safe(container_outer)
    return ''


@register.inclusion_tag('global/partials/_create-form-button.html')
def load_create_button(
    user: User, namespace: str, label: str, dispatcher: Any = None, id_field: str = 'pk'
):
    """Controls the loading of create button inside HTML pages
    Args:
        user (User): User object of currently logged user
        namespace (str): Namespace that points to a URL
        label (str): Label to be placed inside button element
        dispatcher (Any, optional): The dispatcher value to be appended to provided namespace
        id_field (str, optional): The dispatcher field to be appended to provided namespace
    Returns:
        dict: Dict object to be sent to form button partial
    """
    if dispatcher:
        return {
            'user': user,
            'namespace': reverse(namespace, kwargs={id_field: dispatcher}),
            'label': label,
        }
    return {'user': user, 'namespace': reverse(namespace), 'label': label}


@register.filter
def filename(value):
    """Returns
    """
    return path.basename(value.file.name)

from math import ceil
from os import path
from typing import Any

from django import template
from django.core.files import File
from django.core.paginator import Paginator
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
def filename(file: File):
    """Returns the final component of a file path.

    Args:
        file (File): File object to extract the name from.
    """
    return path.basename(file.name)


def get_custom_page_range(p, **kwargs):
    paginator = Paginator(p.object_list, p.per_page)
    paginator.ELLIPSIS = '...'  # type: ignore
    elided_page_range = paginator.get_elided_page_range(**kwargs)  # type: ignore
    return elided_page_range


@register.inclusion_tag('global/partials/_pagination2.html')
def load_paginator_partial(p, number, on_each_side=2, on_ends=1):
    if number == p.page_range.start or number == p.page_range.stop - 1:
        on_each_side = 2
    elif number == p.page_range.start + 1 or number == p.page_range.stop - 2:
        on_each_side = 3
    else:
        on_each_side = 1
    page_range = list(
        get_custom_page_range(
            p, number=number, on_each_side=on_each_side, on_ends=on_ends
        )
    )
    if '...' in page_range:
        page_range.remove('...')
    return_range = {}
    if p.num_pages <= 4:
        return_range |= {'middle_range': page_range}
    else:
        return_range |= {
            'start_range': page_range[0],
            'middle_range': page_range[1:-1],
            'end_range': page_range[-1],
        }
    return return_range


@register.inclusion_tag('global/partials/_pagination3.html')
def make_pagination_range(paginator, current_page, additional_params=''):
    page_range = paginator.page_range
    qty_pages = 4
    middle_range = ceil(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)
    start_range_offset = abs(start_range) if start_range < 0 else 0
    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset
    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)
    pagination = page_range[start_range:stop_range]
    pagination_range = {
        'pagination': pagination,
        'page_range': page_range,
        'qty_page': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
        'additional_url_params': additional_params,
    }
    return pagination_range

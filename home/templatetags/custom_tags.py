from django import template
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def load_regs(db_regs: QuerySet, reg, div, empty):
    """Load regs inside a Django QuerySet of returns error message if none exists.

    Args:
        db_regs (QuerySet): QuerySet object related to model query.
        reg (str): Object variable name to be used during iteration.
        div (str): Div class name for objects wrapping.
        empty (str): Message to display if the given QuerySet is empty.

    Returns:
        SafeString: Output string to be appended on html page.
    """
    template = 'archive/partials/_archive-item.html'
    container = '<div class={}>{}</div>'
    if db_regs:
        process = (render_to_string(template, {reg: i}) for i in db_regs)
        final_content = ''.join(process)
        container = container.format(div, final_content)
        return mark_safe(container)
    else:
        return mark_safe(f'<p class="nothing-found">{empty}</p>')


@register.simple_tag()
def check_error(field):
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
def load_create_button(user, namespace, label):
    return {'user': user, 'namespace': reverse(namespace), 'label': label}

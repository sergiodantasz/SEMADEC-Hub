from django.urls import resolve, reverse
from pytest import mark

from archive import views


def test_archive_viewname_redirects_to_archive_view():
    view = resolve(reverse('archive:home'))
    assert view.func is views.archive


def test_archive_detailed_viewname_redirects_to_archive_detailed_view():
    view = resolve(reverse('archive:archive_detailed', kwargs={'slug': 'test-slug'}))
    assert view.func is views.archive_detailed


@mark.skip
def test_archive_submit_viewname_redirects_to_archive_submit_view():
    view_new = resolve(reverse('archive:submitarchive'))
    assert view_new.func is views.submit_archive


@mark.skip
def test_archive_create_viewname_redirects_to_archive_create_view():
    view_new = resolve(reverse('archive:createarchive'))
    assert view_new.func is views.create_archive

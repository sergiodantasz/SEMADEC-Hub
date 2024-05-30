from django.urls import resolve, reverse
from pytest import mark

from apps.archive import views


def test_archive_viewname_redirects_to_archive_view():
    view = resolve(reverse('archive:home'))
    assert view.func is views.archive_collection


def test_archive_detailed_viewname_redirects_to_archive_detailed_view():
    view = resolve(reverse('archive:detailed', kwargs={'slug': 'test-slug'}))
    assert view.func is views.view_archive_collection


def test_archive_create_viewname_redirects_to_archive_create_view():
    view_new = resolve(reverse('archive:create'))
    assert view_new.func is views.create_archive_collection


@mark.skip
def test_archive_search_viewname_redirects_to_archive_create_view():
    view_new = resolve(reverse('archive:search'))
    assert view_new.func is views.search_archive_collection


def test_archive_edit_viewname_redirects_to_archive_edit_view():
    view_new = resolve(reverse('archive:edit', kwargs={'slug': 'test'}))
    assert view_new.func is views.edit_archive_collection


def test_archive_delete_viewname_redirects_to_archive_delete_view():
    view_new = resolve(reverse('archive:delete', kwargs={'slug': 'test'}))
    assert view_new.func is views.delete_archive_collection


def test_archive_image_delete_viewname_redirects_to_archive_image_delete_view():
    view_new = resolve(reverse('archive:image:delete', kwargs={'pk': 1}))
    assert view_new.func is views.delete_image

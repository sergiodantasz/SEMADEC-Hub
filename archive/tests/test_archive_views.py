from django.urls import resolve, reverse

from archive import views


def test_archive_viewname_redirects_to_archive_view():
    view = resolve(reverse('archive:archive'))
    assert view.func is views.archive

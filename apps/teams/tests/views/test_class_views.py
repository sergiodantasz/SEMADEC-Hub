from django.urls import resolve, reverse

from apps.teams.views import views_classes as views


def test_classes_home_viewname_redirects_to_classes_list_view():
    view = resolve(reverse('teams:classes:home'))
    assert view.func.view_class is views.ClassListView


def test_classes_search_viewname_redirects_to_classes_search_view():
    view = resolve(reverse('teams:classes:search'))
    assert view.func.view_class is views.ClassSearchView


def test_classes_create_viewname_redirects_to_classes_create_view():
    view = resolve(reverse('teams:classes:create'))
    assert view.func.view_class is views.ClassCreateView


def test_classes_edit_viewname_redirects_to_classes_edit_view():
    view = resolve(reverse('teams:classes:edit', kwargs={'slug': 'test'}))
    assert view.func.view_class is views.ClassEditView


def test_classes_delete_viewname_redirects_to_classes_Delete_view():
    view = resolve(reverse('teams:classes:delete', kwargs={'slug': 'test'}))
    assert view.func.view_class is views.ClassDeleteView

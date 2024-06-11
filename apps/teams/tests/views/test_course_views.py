from django.urls import resolve, reverse

from apps.teams.views import views_courses as views


def test_courses_home_viewname_redirects_to_courses_list_view():
    view = resolve(reverse('teams:courses:home'))
    assert view.func.view_class is views.CourseListView


def test_courses_search_viewname_redirects_to_courses_search_view():
    view = resolve(reverse('teams:courses:search'))
    assert view.func.view_class is views.CourseSearchView


def test_courses_create_viewname_redirects_to_courses_create_view():
    view = resolve(reverse('teams:courses:create'))
    assert view.func.view_class is views.CourseCreateView


def test_courses_edit_viewname_redirects_to_courses_edit_view():
    view = resolve(reverse('teams:courses:edit', kwargs={'slug': 'test'}))
    assert view.func.view_class is views.CourseEditView


def test_courses_delete_viewname_redirects_to_courses_Delete_view():
    view = resolve(reverse('teams:courses:delete', kwargs={'slug': 'test'}))
    assert view.func.view_class is views.CourseDeleteView

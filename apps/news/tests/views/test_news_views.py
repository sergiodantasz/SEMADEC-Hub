from django.urls import resolve, reverse

from apps.news import views


def test_news_list_viewname_redirects_to_news_list_view():
    view = resolve(reverse('news:list'))
    assert view.func.view_class is views.NewsListView


def test_news_search_viewname_redirects_to_news_search_view():
    view = resolve(reverse('news:search'))
    assert view.func.view_class is views.NewsSearchView


def test_news_create_viewname_redirects_to_create_view():
    view = resolve(reverse('news:create'))
    assert view.func.view_class is views.NewsCreateView


def test_delete_viewname_redirects_to_delete_view():
    view = resolve(reverse('news:delete', kwargs={'slug': 'test-slug'}))
    assert view.func.view_class is views.NewsDeleteView


def test_edit_viewname_redirects_to_edit_view():
    view = resolve(reverse('news:edit', kwargs={'slug': 'test-slug'}))
    assert view.func.view_class is views.NewsEditView


def test_view_viewname_redirects_to_view_view():
    view = resolve(reverse('news:view', kwargs={'slug': 'slug-test'}))
    assert view.func.view_class is views.NewsDetailView

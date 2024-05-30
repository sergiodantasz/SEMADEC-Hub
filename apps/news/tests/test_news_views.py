from django.urls import resolve, reverse

from apps.news import views


def test_news_list_viewname_redirects_to_news_list_view():
    view = resolve(reverse('news:list'))
    assert view.func.view_class is views.NewsListView


def test_news_search_viewname_redirects_to_news_search_view():
    view = resolve(reverse('news:search'))
    assert view.func.view_class is views.NewsSearchListView


def test_news_create_viewname_redirects_to_create_news_view():
    view = resolve(reverse('news:create_news'))
    assert view.func is views.create_news


def test_delete_news_viewname_redirects_to_delete_news_view():
    view = resolve(reverse('news:delete_news', kwargs={'slug': 'test-slug'}))
    assert view.func is views.delete_news


def test_edit_news_viewname_redirects_to_edit_news_view():
    view = resolve(reverse('news:edit_news', kwargs={'slug': 'test-slug'}))
    assert view.func is views.edit_news


def test_view_news_viewname_redirects_to_view_news_view():
    view = resolve(reverse('news:view_news', kwargs={'slug': 'slug-test'}))
    assert view.func is views.view_news

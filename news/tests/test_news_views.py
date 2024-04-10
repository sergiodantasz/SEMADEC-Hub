from django.urls import resolve, reverse

from news import views


def test_news_viewname_redirects_to_news_view():
    view = resolve(reverse('news:news'))
    assert view.func is views.news


def test_search_news_viewname_redirects_to_news_search_view():
    view = resolve(reverse('news:search_news'))
    assert view.func is views.search_news


def test_create_news_viewname_redirects_to_create_news_view():
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

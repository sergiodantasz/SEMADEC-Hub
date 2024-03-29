from django.urls import resolve, reverse

from news import views


def test_news_viewname_redirects_to_news_view():
    view = resolve(reverse('news:news'))
    assert view.func is views.news


def test_view_news_viewname_redirects_to_view_news_view():
    view = resolve(reverse('news:view_news', kwargs={'slug': 'slug-test'}))
    assert view.func is views.view_news

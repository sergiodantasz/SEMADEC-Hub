from django.db.models.query import QuerySet
from django.test import RequestFactory
from django.urls import resolve, reverse
from pytest import mark

from apps.competitions.forms import SportForm
from apps.home.tests.factories import TagFactory
from apps.news import views
from apps.users.tests.factories import UserFactory


def test_news_list_view_get_queryset_method_returns_queryset():
    view = views.NewsListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_news_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('news:home'))
    request.resolver_match = resolve(reverse('news:home'))
    response = views.NewsListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_news_search_view_get_queryset_method_returns_queryset(db):
    request = RequestFactory().get(reverse('news:search'))
    request.GET |= {'q': 'test'}
    view = views.NewsSearchView()
    view.setup(request)
    queryset = view.get_queryset()
    assert isinstance(queryset, QuerySet)


def test_news_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('news:search'))
    request.GET |= {'q': 'test'}
    response = views.NewsSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_news_search_view_get_tags_from_url_return_tags(db):
    request = RequestFactory().get(reverse('news:search'))
    request.GET |= {'q': 'test', 'tags': ('tag_test',)}
    view = views.NewsSearchView()
    view.setup(request)
    response = view.get_tags_from_url()
    assert len(response) > 0


def test_news_search_view_get_tags_return_tags(db):
    TagFactory(slug='tag1')
    TagFactory(slug='tag2')
    request = RequestFactory().get(reverse('news:search'))
    request.GET |= {'q': 'test'}
    view = views.NewsSearchView()
    view.setup(request)
    response = view.get_tags(['tag1', 'tag2', '', 'tag2'])
    assert len(response) == 2


def test_news_create_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('news:create'))
    request.resolver_match = resolve(reverse('news:create'))
    request.user = UserFactory(is_admin=True)
    response = views.NewsCreateView.as_view()(request)
    assert isinstance(response.context_data, dict)


@mark.skip
def test_news_create_view(db, news_form_fixture):
    form = news_form_fixture()
    request = RequestFactory().get(reverse('news:create'))
    request.resolver_match = resolve(reverse('news:create'))
    request.user = UserFactory(is_admin=True)
    request._messages = {}
    view = views.NewsCreateView()
    view.setup(request)
    response = view.form_valid(form)
    assert isinstance(response.context_data, dict)

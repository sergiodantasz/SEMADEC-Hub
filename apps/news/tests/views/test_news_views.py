from django.contrib.messages import get_messages
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.test import Client, RequestFactory
from django.urls import resolve, reverse
from pytest import mark
from pytest import raises as assert_raises

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


def test_news_create_view_form_valid_redirects_to_news_home(db, news_form_fixture):
    c = Client()
    user = UserFactory()
    request = c.get(reverse('news:create')).wsgi_request
    request.user = user
    form = news_form_fixture()
    view = views.NewsCreateView()
    view.setup(request)
    response = view.form_valid(form)
    assert response.url == reverse('news:home')


def test_news_edit_view_context_data_is_dict(db, news_fixture):
    obj = news_fixture()
    request = RequestFactory().get(reverse('news:edit', kwargs={'slug': obj.slug}))
    view = views.NewsEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)


def test_news_edit_get_method_raises_permissiondenied_if_user_not_owner(
    db, news_fixture
):
    user1 = UserFactory()
    user2 = UserFactory()
    obj = news_fixture(administrator=user1)
    request = RequestFactory().get(reverse('news:edit', kwargs={'slug': obj.slug}))
    request.user = user2
    view = views.NewsEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    with assert_raises(PermissionDenied):
        view.get(request)


def test_news_edit_get_method_returns_status_code_200_if_user_is_owner(
    db, news_fixture
):
    user1 = UserFactory()
    obj = news_fixture(administrator=user1)
    request = RequestFactory().get(reverse('news:edit', kwargs={'slug': obj.slug}))
    request.user = user1
    view = views.NewsEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    response = view.get(request)
    assert response.status_code == 200


def test_news_delete_get_method_shows_error_if_user_not_owner(db, news_fixture):
    user1 = UserFactory()
    user2 = UserFactory()
    obj = news_fixture(administrator=user1)
    c = Client()
    request = c.get(reverse('news:delete', kwargs={'slug': obj.slug})).wsgi_request
    request.user = user2
    view = views.NewsDeleteView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    view.get(request)
    messages = list(get_messages(request))
    assert messages[0].level_tag == 'message-error'


def test_news_delete_get_method_deletes_object_if_user_is_owner(db, news_fixture):
    user1 = UserFactory()
    obj = news_fixture(administrator=user1)
    c = Client()
    request = c.get(reverse('news:delete', kwargs={'slug': obj.slug})).wsgi_request
    request.user = user1
    view = views.NewsDeleteView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    response = view.get(request)
    assert response.url == reverse('news:home')

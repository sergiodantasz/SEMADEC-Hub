from django.db.models.query import QuerySet
from django.test import RequestFactory
from django.urls import resolve, reverse

from apps.competitions import views
from apps.competitions.forms import SportForm
from apps.users.tests.factories import UserFactory


def test_sport_list_view_get_queryset_method_returns_queryset():
    view = views.SportListView()
    assert isinstance(view.get_queryset(), QuerySet)


def test_sport_list_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('competitions:sports:home'))
    request.resolver_match = resolve(reverse('competitions:sports:home'))
    response = views.SportListView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_sports_search_view_get_queryset_method_returns_queryset(db):
    request = RequestFactory().get(reverse('competitions:sports:search'))
    request.GET |= {'q': 'test'}
    view = views.SportSearchView()
    view.setup(request)
    queryset = view.get_queryset()
    assert isinstance(queryset, QuerySet)


def test_sports_search_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('competitions:sports:search'))
    request.GET |= {'q': 'test'}
    response = views.SportSearchView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_sports_create_view_context_data_is_dict(db):
    request = RequestFactory().get(reverse('competitions:sports:create'))
    request.resolver_match = resolve(reverse('competitions:sports:create'))
    request.user = UserFactory(is_admin=True)
    response = views.SportCreateView.as_view()(request)
    assert isinstance(response.context_data, dict)


def test_sports_edit_view_context_data_is_dict(db, sport_fixture):
    obj = sport_fixture()
    request = RequestFactory().get(
        reverse('competitions:sports:edit', kwargs={'slug': obj.slug})
    )
    view = views.SportEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)


def test_sports_edit_view_get_form_returns_form(db, sport_fixture):
    obj = sport_fixture()
    request = RequestFactory().get(
        reverse('competitions:sports:edit', kwargs={'slug': obj.slug})
    )
    view = views.SportEditView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    form = view.get_form()
    assert isinstance(form, SportForm)


def test_sports_detail_view_context_data_is_dict(db, sport_fixture):
    obj = sport_fixture()
    request = RequestFactory().get(
        reverse('competitions:sports:detailed', kwargs={'slug': obj.slug})
    )
    view = views.SportDetailView()
    view.setup(request, slug=obj.slug)
    view.object = obj
    context = view.get_context_data()
    assert isinstance(context, dict)

import pytest
from django.conf import settings
from django.utils import timezone
from factory.faker import faker

from apps.competitions.forms import (
    MatchForm,
    MatchTeamForm,
    SportForm,
    TestForm,
    TestTeamForm,
)
from apps.competitions.tests.factories import (
    CategoryFactory,
    MatchFactory,
    MatchWithTeamFactory,
    SportCategoryFactory,
    SportFactory,
    TestWithTeamFactory,
)
from apps.teams.tests.factories import ClassFactory, TeamFactory

fake = faker.Faker('pt_BR')


@pytest.fixture
def category_fixture():
    yield CategoryFactory


@pytest.fixture
def sport_fixture():
    categories = CategoryFactory.create_batch(2)
    caller = lambda **kwargs: SportFactory(categories=categories, **kwargs)  # noqa
    yield caller


@pytest.fixture
def sport_category_fixture():
    caller = lambda **kwargs: SportCategoryFactory(**kwargs)  # noqa
    yield caller


@pytest.fixture
def sport_form_fixture():
    data = {
        'name': 'test name',
        'categories': CategoryFactory.create_batch(2),
    }
    caller = lambda **kwargs: SportForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def test_fixture():
    yield TestWithTeamFactory


@pytest.fixture
def test_form_fixture():
    data = {
        'title': 'test title',
        'description': 'test description',
        'date_time': fake.date_time(tzinfo=timezone.get_current_timezone()),
        'teams': TeamFactory.create_batch(3),
    }
    caller = lambda **kwargs: TestForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def test_team_form_fixture():
    data = {
        'score': 10,
    }
    caller = lambda **kwargs: TestTeamForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def match_fixture():
    yield MatchWithTeamFactory


@pytest.fixture
def match_form_fixture():
    data = {
        'sport_category': SportCategoryFactory(),
        'date_time': fake.date_time(tzinfo=timezone.get_current_timezone()),
        'teams': TeamFactory.create_batch(3),
    }
    caller = lambda **kwargs: MatchForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def match_team_form_fixture():
    data = {
        'score': 10,
    }
    caller = lambda **kwargs: MatchTeamForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def sport_with_categories_fixture():
    reg = SportFactory.create(categories=(category_fixture(),))
    yield reg


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

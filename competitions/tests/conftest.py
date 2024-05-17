import pytest
from django.conf import settings

from competitions.tests.factories import (
    CategoryFactory,
    MatchFactory,
    MatchWithTeamFactory,
    SportFactory,
    TestWithTeamFactory,
)


@pytest.fixture
def category_fixture():
    yield CategoryFactory


@pytest.fixture
def sport_fixture():
    categories = CategoryFactory.create_batch(2)
    caller = lambda **kwargs: SportFactory(categories=categories, **kwargs)  # noqa
    yield caller


@pytest.fixture
def match_fixture():
    yield MatchWithTeamFactory


@pytest.fixture
def sport_with_categories_fixture():
    reg = SportFactory.create(categories=(category_fixture(),))
    yield reg


@pytest.fixture
def test_fixture():
    yield TestWithTeamFactory


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

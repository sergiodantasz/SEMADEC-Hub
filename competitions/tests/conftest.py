import pytest
from django.conf import settings

from competitions.tests.factories import (
    CategoryFactory,
    CompetitionFactory,
    SportFactory,
    TestFactory,
    TestOrSportFactory,
)
from editions.tests.factories import (
    ClassFactory,
)

settings.STORAGES['default']['BACKEND'] = 'django.core.files.storage.InMemoryStorage'


@pytest.fixture
def category_fixture():
    yield CategoryFactory


@pytest.fixture
def class_fixture():
    yield ClassFactory


@pytest.fixture
def competition_fixture():
    yield CompetitionFactory


@pytest.fixture
def sport_fixture():
    yield SportFactory


@pytest.fixture
def test_fixture():
    yield TestFactory


@pytest.fixture
def test_or_sport_fixture():
    yield TestOrSportFactory

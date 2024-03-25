import pytest
from django.conf import settings

from competitions.models import Category
from competitions.tests.factories import (
    CategoryFactory,
    SportFactory,
    TestFactory,
)
from editions.tests.factories import (
    ClassFactory,
)

settings.STORAGES['default']['BACKEND'] = 'django.core.files.storage.InMemoryStorage'


@pytest.fixture
def category_fixture():
    yield CategoryFactory
    Category.objects.all().delete()


@pytest.fixture
def class_fixture():
    yield ClassFactory


# @pytest.fixture
# def competition_fixture():
#     yield CompetitionFactory


@pytest.fixture
def sport_fixture():
    yield SportFactory


@pytest.fixture
def sport_with_categories_fixture():
    reg = SportFactory.create(categories=(category_fixture(),))
    yield reg
    reg.delete()
    ...


@pytest.fixture
def test_fixture():
    yield TestFactory


# @pytest.fixture
# def test_or_sport_fixture():
#     yield TestOrSportFactory

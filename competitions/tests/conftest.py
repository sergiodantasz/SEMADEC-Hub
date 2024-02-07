import pytest

from competitions.tests.factories import (
    CategoryFactory,
    CompetitionFactory,
    SportFactory,
    TestFactory,
    TestOrSportFactory,
)
from editions.tests.factories import (
    ClassFactory,
    TeamWithCompetitionFactory,
)


@pytest.fixture
def category_fixture():
    return CategoryFactory


@pytest.fixture
def class_fixture():
    return ClassFactory


@pytest.fixture
def team_with_competition_fixture():
    def inner(**kwargs):
        factory = TeamWithCompetitionFactory.create(
            classes=(class_fixture(),), **kwargs
        )
        return factory

    return inner


@pytest.fixture
def competition_fixture():
    return CompetitionFactory


@pytest.fixture
def sport_fixture():
    return SportFactory


@pytest.fixture
def test_fixture():
    return TestFactory


@pytest.fixture
def test_or_sport_fixture():
    return TestOrSportFactory

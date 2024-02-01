import pytest

from competitions.tests.factories import (
    CategoryFactory,
    CompetitionFactory,
    SportFactory,
    TestFactory,
    TestOrSportFactory,
)


@pytest.fixture
def category_fixture():
    return CategoryFactory


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

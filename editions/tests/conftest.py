import pytest
from django.conf import settings

from competitions.tests.factories import (
    MatchTeamFactory,
    TestTeamFactory,
    TestWithTeamFactory,
)
from editions.tests.factories import (
    ClassFactory,
    CourseFactory,
    EditionFactory,
    EditionTeamFactory,
    EditionWithTeamFactory,
    TeamFactory,
)


@pytest.fixture
def edition_fixture():
    yield EditionWithTeamFactory


@pytest.fixture
def class_fixture():
    yield ClassFactory


@pytest.fixture
def course_fixture():
    yield CourseFactory


@pytest.fixture
def edition_team_fixture():
    yield EditionTeamFactory


@pytest.fixture
def match_team_fixture():
    yield MatchTeamFactory


def test_fixture():
    yield TestWithTeamFactory


@pytest.fixture
def test_team_fixture():
    yield TestTeamFactory


@pytest.fixture
def team_fixture():
    yield TeamFactory


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

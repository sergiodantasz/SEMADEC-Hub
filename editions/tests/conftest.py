import pytest
from django.conf import settings

from competitions.tests.factories import (
    MatchTeamFactory,
    TestTeamFactory,
    TestWithTeamFactory,
)
from editions.tests.factories import (
    EditionTeamFactory,
    EditionWithTeamFactory,
)


@pytest.fixture
def edition_fixture():
    yield EditionWithTeamFactory


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


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

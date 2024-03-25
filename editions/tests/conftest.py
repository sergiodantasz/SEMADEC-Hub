import pytest
from django.conf import settings

from competitions.tests.factories import EditionFactory
from editions.tests.factories import (
    ClassFactory,
    CourseFactory,
    TeamEditionFactory,
    TeamFactory,
    TeamWithMatchesAndTestsAndEditionsFactory,
)


@pytest.fixture
def class_fixture():
    yield ClassFactory


@pytest.fixture
def course_fixture():
    yield CourseFactory


@pytest.fixture
def edition_fixture():
    yield EditionFactory


# @pytest.fixture
# def team_competition_fixture():
#     yield TeamCompetitionFactory


@pytest.fixture
def team_edition_fixture():
    yield TeamEditionFactory


# @pytest.fixture
# def team_fixture():
#     yield TeamWithCompetitionsAndEditionsFactory


@pytest.fixture
def team_fixture():
    yield TeamWithMatchesAndTestsAndEditionsFactory


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

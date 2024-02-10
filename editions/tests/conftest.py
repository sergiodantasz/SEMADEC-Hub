import pytest

from competitions.tests.factories import EditionFactory
from editions.tests.factories import (
    ClassFactory,
    CourseFactory,
    TeamCompetitionFactory,
    TeamEditionFactory,
    TeamFactory,
    TeamWithCompetitionsAndEditionsFactory,
)


@pytest.fixture
def class_fixture():
    return ClassFactory


@pytest.fixture
def course_fixture():
    return CourseFactory


@pytest.fixture
def edition_fixture():
    return EditionFactory


@pytest.fixture
def team_competition_fixture():
    return TeamCompetitionFactory


@pytest.fixture
def team_edition_fixture():
    return TeamEditionFactory


@pytest.fixture
def team_fixture():
    return TeamWithCompetitionsAndEditionsFactory

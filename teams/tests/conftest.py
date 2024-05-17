import pytest
from django.conf import settings

from teams.tests.factories import ClassFactory, CourseFactory, TeamFactory


@pytest.fixture
def class_fixture():
    yield ClassFactory


@pytest.fixture
def course_fixture():
    yield CourseFactory


@pytest.fixture
def team_fixture():
    yield TeamFactory


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

import pytest
from django.conf import settings

from apps.teams.forms import ClassForm, CourseForm, TeamForm
from apps.teams.tests.factories import ClassFactory, CourseFactory, TeamFactory


@pytest.fixture
def course_fixture():
    yield CourseFactory


@pytest.fixture
def course_form_fixture():
    data = {
        'name': 'test',
    }
    caller = lambda **kwargs: CourseForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def class_fixture():
    yield ClassFactory


@pytest.fixture
def class_form_fixture():
    data = {
        'name': 'test',
        'course': CourseFactory(),
    }
    caller = lambda **kwargs: ClassForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def team_fixture():
    yield TeamFactory


@pytest.fixture
def team_form_fixture():
    data = {
        'name': 'test',
        'classes': ClassFactory.create_batch(3),
    }
    caller = lambda **kwargs: TeamForm(data=data | kwargs)  # noqa
    yield caller


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

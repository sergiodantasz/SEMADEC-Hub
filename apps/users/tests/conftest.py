import pytest
from django.conf import settings

from apps.users.tests.factories import (
    CampusFactory,
    UserFactory,
)


@pytest.fixture
def campus_fixture():
    yield CampusFactory


@pytest.fixture
def user_fixture():
    yield UserFactory


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

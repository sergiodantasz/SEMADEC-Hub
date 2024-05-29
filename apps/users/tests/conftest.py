import pytest
from django.conf import settings

from users.tests.factories import (
    CampusFactory,
    EmailFactory,
    UserFactory,
)


@pytest.fixture
def campus_fixture():
    yield CampusFactory


@pytest.fixture
def user_fixture():
    yield UserFactory


@pytest.fixture
def email_fixture():
    yield EmailFactory


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

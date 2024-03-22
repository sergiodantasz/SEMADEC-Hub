import pytest
from django.conf import settings

from users.tests.factories import (
    CampusFactory,
    EmailFactory,
    UserFactory,
)

settings.STORAGES['default']['BACKEND'] = 'django.core.files.storage.InMemoryStorage'


@pytest.fixture
def campus_fixture():
    yield CampusFactory


@pytest.fixture
def user_fixture():
    user = UserFactory
    yield user


@pytest.fixture
def email_fixture():
    yield EmailFactory

import pytest
from django.conf import settings

from apps.home.tests.factories import TagFactory


@pytest.fixture
def tag_fixture():
    yield TagFactory


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

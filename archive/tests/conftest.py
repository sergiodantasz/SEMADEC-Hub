import pytest
from django.conf import settings

from archive.tests.factories import CollectionFactory, FileFactory

settings.STORAGES['default']['BACKEND'] = 'django.core.files.storage.InMemoryStorage'


@pytest.fixture
def collection_fixture():
    yield CollectionFactory


@pytest.fixture
def file_fixture():
    yield FileFactory

import pytest
from django.conf import settings

from documents.tests.factories import DocumentFactory

settings.STORAGES['default']['BACKEND'] = 'django.core.files.storage.InMemoryStorage'


@pytest.fixture
def document_fixture():
    yield DocumentFactory

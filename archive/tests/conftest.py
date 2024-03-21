import pytest
from django.conf import settings

from archive.tests.factories import CollectionFactory, FileFactory

settings.STORAGES['default']['BACKEND'] = 'django.core.files.storage.InMemoryStorage'


@pytest.fixture
def file_fixture():
    return FileFactory


@pytest.fixture
def collection_fixture():  # noqa: F811
    def inner(**kwargs):
        factory = CollectionFactory.create(
            files=(FileFactory(),),  # Change fixture calling
            **kwargs,
        )
        return factory

    return inner

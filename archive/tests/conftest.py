import pytest
from django.conf import settings

from archive.tests.factories import CollectionFactory, FileFactory
from home.tests.factories import TagFactory


@pytest.fixture
def file_fixture():
    return FileFactory


@pytest.fixture
def collection_fixture():
    files = FileFactory.create_batch(5)
    tags = TagFactory.create_batch(5)
    caller = lambda **kwargs: CollectionFactory(files=files, tags=tags, **kwargs)  # noqa
    yield caller


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

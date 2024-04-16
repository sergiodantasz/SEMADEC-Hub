import pytest
from django.conf import settings

from archive.tests.factories import CollectionFactory, ImageFactory
from home.tests.factories import TagFactory


@pytest.fixture
def collection_fixture():
    tags = TagFactory.create_batch(5)
    caller = lambda **kwargs: CollectionFactory(tags=tags, **kwargs)  # noqa
    yield caller


@pytest.fixture
def image_fixture():
    caller = lambda size=1, **kwargs: ImageFactory.create_batch(size, **kwargs)  # noqa
    yield caller


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

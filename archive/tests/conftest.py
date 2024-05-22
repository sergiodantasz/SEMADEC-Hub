import pytest
from django.conf import settings

from archive.forms import ImageCollectionForm, ImageForm
from archive.tests.factories import CollectionFactory, ImageFactory
from home.tests.factories import TagFactory


@pytest.fixture
def collection_fixture():
    tags = TagFactory.create_batch(5)
    caller = lambda **kwargs: CollectionFactory(tags=tags, **kwargs)  # noqa
    yield caller


@pytest.fixture
def image_collection_form_fixture():
    data = {
        'cover': ImageFactory(),
        'title': 'Título teste',
        'collection_type': 'image',
        'tags': TagFactory.create_batch(2),
    }
    caller = lambda **kwargs: ImageCollectionForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def image_fixture():
    caller = lambda size=1, **kwargs: ImageFactory.create_batch(size, **kwargs)  # noqa
    yield caller


@pytest.fixture
def image_form_fixture():
    data = {'images': ImageFactory()}
    caller = lambda **kwargs: ImageForm(data=data | kwargs)  # noqa
    yield caller


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

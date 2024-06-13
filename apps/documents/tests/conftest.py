import pytest
from django.conf import settings
from factory.django import FileField

from apps.documents.forms import DocumentCollectionForm, DocumentForm
from apps.documents.tests.factories import DocumentFactory
from apps.home.tests.factories import TagFactory


@pytest.fixture(scope='session')
def document_fixture():
    caller = lambda size=1, **kwargs: DocumentFactory.create_batch(size, **kwargs)  # noqa
    yield caller


@pytest.fixture
def document_collection_form_fixture():
    data = {
        'title': 'test',
        'collection_type': 'document',
        'tags': TagFactory.create_batch(3),
    }
    caller = lambda **kwargs: DocumentCollectionForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def document_form_fixture():
    data = {
        'documents': FileField(),
    }
    caller = lambda **kwargs: DocumentForm(data=data | kwargs)  # noqa
    yield caller


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

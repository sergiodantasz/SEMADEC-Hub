import pytest
from django.conf import settings

from documents.tests.factories import DocumentFactory


@pytest.fixture(scope='session')
def document_fixture():
    caller = lambda size=1, **kwargs: DocumentFactory.create_batch(size, **kwargs)  # noqa
    yield caller


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

import pytest
from django.conf import settings

from news.tests.factories import NewsFactory


@pytest.fixture
def news_fixture():
    yield NewsFactory


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

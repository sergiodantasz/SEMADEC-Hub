import pytest
from django.conf import settings

from news.tests.factories import NewsFactory

settings.STORAGES['default']['BACKEND'] = 'django.core.files.storage.InMemoryStorage'


@pytest.fixture
def news_fixture():
    yield NewsFactory

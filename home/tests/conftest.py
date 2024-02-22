import pytest
from django.conf import settings

from archive.tests.conftest import collection_fixture
from documents.tests.conftest import document_fixture
from home.tests.factories import TagFactory
from news.tests.conftest import news_fixture

settings.STORAGES['default']['BACKEND'] = 'django.core.files.storage.InMemoryStorage'


@pytest.fixture
def tag_fixture(news_fixture, collection_fixture, document_fixture):  # noqa: F811
    def inner(**kwargs):
        factory = TagFactory.create(
            news=(news_fixture(),),
            collection=(collection_fixture(),),
            document=(document_fixture(),),
            **kwargs,
        )
        return factory

    yield inner

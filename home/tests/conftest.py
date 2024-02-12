import pytest

from home.tests.factories import TagFactory


@pytest.fixture
def tag_fixture(news_fixture, collection_fixture, document_fixture):
    def inner(**kwargs):
        factory = TagFactory.create(
            news=(news_fixture(),),
            collection=(collection_fixture(),),
            document=(document_fixture(),),
            **kwargs,
        )
        return factory

    return inner

import pytest

from news.tests.factories import NewsFactory


@pytest.fixture
def news_fixture():
    return NewsFactory

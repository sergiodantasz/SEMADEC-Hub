import pytest
from django.conf import settings

from home.tests.factories import TagFactory
from news.tests.factories import NewsFactory


@pytest.fixture
def news_fixture():
    tags = TagFactory.create_batch(5)
    caller = lambda **kwargs: NewsFactory(tags=tags, **kwargs)  # noqa
    yield caller


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

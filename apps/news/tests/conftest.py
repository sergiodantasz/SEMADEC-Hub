import pytest
from django.conf import settings
from factory.django import ImageField

from apps.home.tests.factories import TagFactory
from apps.news.forms import NewsForm
from apps.news.tests.factories import NewsFactory


@pytest.fixture
def news_fixture():
    tags = TagFactory.create_batch(5)
    caller = lambda **kwargs: NewsFactory(tags=tags, **kwargs)  # noqa
    yield caller


@pytest.fixture
def news_form_fixture():
    data = {
        'cover': ImageField(),
        'title': 'title',
        'excerpt': 'excerpt',
        'content': 'content',
        'tags': TagFactory.create_batch(3),
    }
    caller = lambda **kwargs: NewsForm(data=data | kwargs)  # noqa
    yield caller


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

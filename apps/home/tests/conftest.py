import pytest
from django.conf import settings

from apps.home.forms import TagForm
from apps.home.tests.factories import TagFactory


@pytest.fixture
def tag_fixture():
    yield TagFactory


@pytest.fixture
def tag_form_fixture():
    data = {
        'name': 'test',
    }
    caller = lambda **kwargs: TagForm(data=data | kwargs)  # noqa
    yield caller


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )

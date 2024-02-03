import pytest

from archive.tests.factories import CollectionFactory, FileFactory
from home.tests.conftest import tag_fixture


@pytest.fixture
def collection_fixture(tag_fixture):  # noqa: F811
    def inner(**kwargs):
        # ...
        factory = CollectionFactory.create(tags=(tag_fixture(),), **kwargs)
        return factory

    return inner


@pytest.fixture
def file_fixture():
    return FileFactory

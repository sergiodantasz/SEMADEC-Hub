import pytest

from archive.tests.factories import CollectionFactory, FileFactory


@pytest.fixture
def collection_fixture():
    return CollectionFactory


@pytest.fixture
def file_fixture():
    return FileFactory

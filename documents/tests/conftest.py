import pytest

from documents.tests.factories import DocumentFactory


@pytest.fixture
def document_fixture():
    return DocumentFactory

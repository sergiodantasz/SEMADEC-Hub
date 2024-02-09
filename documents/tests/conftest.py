import pytest

from documents.tests.factories import DocumentFactory
from home.tests.conftest import tag_fixture


@pytest.fixture
def document_fixture(tag_fixture):  # noqa: F811
    def inner(**kwargs):
        factory = DocumentFactory.create(tags=(tag_fixture(),), **kwargs)
        return factory

    return inner

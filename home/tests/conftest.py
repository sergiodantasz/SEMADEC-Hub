import pytest

from home.tests.factories import TagFactory


@pytest.fixture
def tag_fixture():
    return TagFactory

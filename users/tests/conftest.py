import pytest

from users.tests.factories import (
    AdministratorFactory,
    CampusFactory,
    UserFactory,
)


@pytest.fixture
def campus_fixture():
    return CampusFactory


@pytest.fixture
def user_fixture():
    return UserFactory


@pytest.fixture
def administrator_fixture():
    return AdministratorFactory

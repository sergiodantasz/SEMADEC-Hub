import pytest
from faker import Faker

from users.tests.factories.factories_users import (
    AdministratorFactory,
    CampusFactory,
    UserFactory,
)

fake = Faker()


@pytest.fixture
def administrator_fixture():
    return AdministratorFactory()


@pytest.fixture
def campus_fixture():
    return CampusFactory()


@pytest.fixture()
def user_fixture():
    return UserFactory()

import pytest

from users.tests.factories import (
    AdministratorFactory,
    CampusFactory,
    EmailFactory,
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


@pytest.fixture
def email_fixture():
    return EmailFactory

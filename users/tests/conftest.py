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


@pytest.fixture
def user_fixture_data(campus_fixture, course_fixture):
    return {
        'registration': fake.random_number(digits=14),
        'campus': campus_fixture,
        'course': ...,
        'full_name': ...,
        'first_name': ...,
        'last_name': ...,
        'cpf': ...,
        'link_type': ...,
        'sex': ...,
        'date_of_birth': ...,
        'photo_url': ...,
    }


@pytest.fixture
def user_fixture(user_fixture_data):
    return UserFactory(**user_fixture_data)

from django.core.exceptions import ValidationError
from pytest import raises as assert_raises

from users.tests.factories import UserFactory


def test_user_model_registration_has_max_length_14(db, user_fixture):
    user = UserFactory(registration='A' * 20)
    with assert_raises(ValidationError):
        user.full_clean()

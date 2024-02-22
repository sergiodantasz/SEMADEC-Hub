from django.core.exceptions import ValidationError
from pytest import raises as assert_raises


def test_user_model_registration_has_max_length_14(db, user_fixture):
    user = user_fixture(registration='A' * 15)
    with assert_raises(ValidationError):
        user.full_clean()

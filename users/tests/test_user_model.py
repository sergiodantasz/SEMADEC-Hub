from django.core.exceptions import ValidationError
from pytest import raises as assert_raises


def test_user_model_registration_has_max_length_14(db, user_fixture):
    reg = user_fixture(registration='A' * 15)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_user_model_dunder_str_method_returns_user_full_name_and_registration(
    db, user_fixture
):
    reg = user_fixture()
    assert str(reg) == f'{reg.full_name} ({reg.registration})'

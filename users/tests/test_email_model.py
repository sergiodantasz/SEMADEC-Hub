from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import mark
from pytest import raises as assert_raises


@mark.skip
def test_email_model_user_db_column_is_user_registration(db, email_fixture):
    reg = email_fixture()
    assert hasattr(reg, 'user_registration')


def test_email_model_address_is_unique(db, email_fixture):
    with assert_raises(IntegrityError):
        reg1 = email_fixture(address='test@test.com')
        reg2 = email_fixture(address='test@test.com')


def test_email_model_email_type_has_max_length_15(db, email_fixture):
    reg = email_fixture(email_type='a' * 16)
    with assert_raises(ValidationError):
        reg.full_clean()


@mark.skip
def test_email_model_email_type_db_column_is_type(db, email_fixture):
    reg = email_fixture()
    assert hasattr(reg, 'type')

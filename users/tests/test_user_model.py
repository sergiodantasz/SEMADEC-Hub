from django.core.exceptions import ValidationError
from django.db import IntegrityError
from pytest import raises as assert_raises


def test_user_model_registration_has_max_length_14(db, user_fixture):
    reg = user_fixture(registration='A' * 15)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_user_model_dunder_str_method_returns_user_full_name_and_registration(
    db, user_fixture
):
    reg = user_fixture()
    assert str(reg) == f'{reg.full_name}'


def test_user_model_personal_email_is_unique(db, user_fixture):
    with assert_raises(IntegrityError):
        reg1 = user_fixture(personal_email='personal@test.com')
        reg2 = user_fixture(personal_email='personal@test.com')


def test_user_model_personal_email_has_max_length_250(db, user_fixture):
    reg = user_fixture(personal_email='a' * 242 + '@test.com')
    with assert_raises(ValidationError):
        reg.full_clean()


def test_user_model_school_email_is_unique(db, user_fixture):
    with assert_raises(IntegrityError):
        reg1 = user_fixture(school_email='school@test.com')
        reg2 = user_fixture(school_email='school@test.com')


def test_user_model_school_email_has_max_length_250(db, user_fixture):
    reg = user_fixture(school_email='a' * 242 + '@test.com')
    with assert_raises(ValidationError):
        reg.full_clean()


def test_user_model_academic_email_is_unique(db, user_fixture):
    with assert_raises(IntegrityError):
        reg1 = user_fixture(school_email='academic@test.com')
        reg2 = user_fixture(school_email='academic@test.com')


def test_user_model_academic_email_has_max_length_250(db, user_fixture):
    reg = user_fixture(academic_email='a' * 242 + '@test.com')
    with assert_raises(ValidationError):
        reg.full_clean()

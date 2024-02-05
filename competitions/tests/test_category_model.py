from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_category_model_name_has_max_length_15(db, category_fixture):
    reg = category_fixture(name='a' * 16)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_category_model_name_is_unique(db, category_fixture):
    with assert_raises(IntegrityError):
        reg1 = category_fixture(name='duplicated name')
        reg2 = category_fixture(name='duplicated name')


def test_category_model_name_cannot_be_null(db, category_fixture):
    with assert_raises(IntegrityError):
        reg = category_fixture(name=None)


def test_category_model_name_cannot_be_blank(db, category_fixture):
    reg = category_fixture(name='')
    with assert_raises(ValidationError):
        reg.full_clean()

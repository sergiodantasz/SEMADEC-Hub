from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_tag_model_name_max_length_is_50(db, tag_fixture):
    reg = tag_fixture(name='a' * 51)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_tag_model_name_is_unique(db, tag_fixture):
    with assert_raises(IntegrityError):
        reg1 = tag_fixture(name='john doe')
        reg2 = tag_fixture(name='john doe')


def test_tag_model_slug_max_length_is_75(db, tag_fixture):
    reg = tag_fixture(slug='a' * 76)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_tag_model_slug_is_unique(db, tag_fixture):
    with assert_raises(IntegrityError):
        reg1 = tag_fixture(slug='test-slug')
        reg2 = tag_fixture(slug='test-slug')

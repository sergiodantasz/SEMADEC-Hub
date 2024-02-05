from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_file_model_content_is_unique(db, file_fixture):
    with assert_raises(IntegrityError):
        reg1 = file_fixture(content='/test/fixture.py')
        reg1 = file_fixture(content='/test/fixture.py')


def test_file_model_content_cannot_be_null(db, file_fixture):
    reg = file_fixture(content=None)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_file_model_content_cannot_be_blank(db, file_fixture):
    reg = file_fixture(content='')
    with assert_raises(ValidationError):
        reg.full_clean()

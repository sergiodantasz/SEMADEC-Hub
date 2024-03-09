from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_file_model_display_name_has_max_length_225(db, file_fixture):
    reg = file_fixture(display_name='a' * 226)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_file_model_display_name_can_be_null(db, file_fixture):
    reg = file_fixture(display_name=None)
    reg.full_clean()
    assert reg.display_name is None


def test_file_model_display_name_can_be_blank(db, file_fixture):
    reg = file_fixture(display_name='')
    reg.full_clean()
    assert reg.display_name == ''


def test_file_model_content_is_unique(db, file_fixture):
    with assert_raises(IntegrityError):
        reg1 = file_fixture(content='/test/fixture.py')
        reg1 = file_fixture(content='/test/fixture.py')


def test_file_model_dunder_str_method_returns_file_content_name(db, file_fixture):
    reg = file_fixture()
    assert str(reg) == reg.content.name

from django.core.exceptions import ValidationError
from pytest import raises as assert_raises


def test_class_model_course_db_column_is_course_id(db, class_fixture):
    reg = class_fixture()
    assert hasattr(reg, 'course_id')


def test_class_model_entry_year_is_integer(db, class_fixture):
    reg = class_fixture()
    assert isinstance(reg.entry_year, int)


def test_class_model_entry_year_is_positive(db, class_fixture):
    reg = class_fixture()
    assert reg.entry_year > 0


def test_class_model_entry_year_minimum_value_is_2000(db, class_fixture):
    reg = class_fixture(entry_year=1999)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_class_model_entry_year_maximum_value_is_3000(db, class_fixture):
    reg = class_fixture(entry_year=3001)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_class_model_course_can_be_null(db, class_fixture):
    reg = class_fixture(course=None)
    assert reg.course is None


def test_class_model_dunder_str_method_returns_class_course_name(db, class_fixture):
    reg = class_fixture()
    assert str(reg) == reg.name

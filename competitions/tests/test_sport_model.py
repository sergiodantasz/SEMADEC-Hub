from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_sport_model_name_has_max_length_30(db, sport_fixture):
    reg = sport_fixture(name='a' * 31)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_sport_model_category_db_column_is_category_id(db, sport_fixture):
    reg = sport_fixture()
    assert hasattr(reg, 'category_id')


def test_test_model_date_time_can_be_null(db, sport_fixture):
    reg = sport_fixture(date_time=None)
    assert reg.date_time is None


def test_sport_model_date_time_default_value_is_none(db, sport_fixture):
    reg = sport_fixture()
    assert reg.date_time is None


def test_sport_model_dunder_str_method_returns_sport_name(db, sport_fixture):
    reg = sport_fixture()
    assert str(reg) == reg.name

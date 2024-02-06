from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_sport_model_name_has_max_length_30(db, sport_fixture):
    reg = sport_fixture(name='a' * 31)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_sport_model_name_cannot_be_null(db, sport_fixture):
    with assert_raises(IntegrityError):
        reg = sport_fixture(name=None)


def test_sport_model_name_cannot_be_blank(db, sport_fixture):
    reg = sport_fixture(name='')
    with assert_raises(ValidationError):
        reg.full_clean()


def test_sport_model_date_time_cannot_be_blank(db, sport_fixture):
    with assert_raises(ValidationError):
        reg = sport_fixture(date_time='')


def test_sport_model_date_time_default_value_is_none(db, sport_fixture):
    reg = sport_fixture()
    assert reg.date_time is None

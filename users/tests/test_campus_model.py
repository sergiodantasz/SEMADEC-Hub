from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_campus_model_acronym_can_be_overwritten(db, campus_fixture):
    campus = campus_fixture(acronym='BR')
    assert campus.acronym == 'BR'


def test_campus_model_acronym_has_max_length_4(db, campus_fixture):
    campus = campus_fixture(acronym='A' * 5)
    with assert_raises(ValidationError):
        campus.full_clean()


def test_campus_model_name_is_unique(db, campus_fixture):
    with assert_raises(IntegrityError):
        campus1 = campus_fixture(name='Currais Novos')
        campus2 = campus_fixture(name='Currais Novos')


def test_campus_model_name_has_max_length_50(db, campus_fixture):
    campus = campus_fixture(name='A' * 51)
    with assert_raises(ValidationError):
        campus.full_clean()


def test_campus_model_name_cannot_be_null(db, campus_fixture):
    with assert_raises(IntegrityError):
        campus = campus_fixture(name=None)


def test_campus_model_name_cannot_be_blank(db, campus_fixture):
    campus = campus_fixture(name='')
    with assert_raises(ValidationError):
        campus.full_clean()

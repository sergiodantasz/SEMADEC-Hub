from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises

from users.tests.factories.factories_users import CampusFactory


def test_campus_model_acronym_can_be_overwritten(db, campus_fixture):
    campus_fixture.acronym = 'BR'
    assert campus_fixture.acronym == 'BR'


def test_campus_model_acronym_has_max_length_4(db, campus_fixture):
    campus_fixture.acronym = 'A' * 5
    with assert_raises(ValidationError):
        campus_fixture.full_clean()


def test_campus_model_name_is_unique(db):
    with assert_raises(IntegrityError):
        CampusFactory(name='Currais Novos')
        CampusFactory(name='Currais Novos')


def test_campus_model_name_has_max_length_50(db, campus_fixture):
    campus_fixture.name = 'A' * 51
    with assert_raises(ValidationError):
        campus_fixture.full_clean()


def test_campus_model_name_cannot_be_null(db, campus_fixture):
    campus_fixture.name = None
    with assert_raises(ValidationError):
        campus_fixture.full_clean()


def test_campus_model_name_cannot_be_blank(db, campus_fixture):
    campus_fixture.name = ''
    with assert_raises(ValidationError):
        campus_fixture.full_clean()

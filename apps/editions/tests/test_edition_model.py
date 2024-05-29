from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import mark
from pytest import raises as assert_raises

from editions.models import Edition
from teams.models import Team


def test_edition_model_year_is_integer(db, edition_fixture):
    reg = edition_fixture()
    assert isinstance(reg.year, int)


def test_edition_model_year_is_positive(db, edition_fixture):
    reg = edition_fixture()
    assert reg.year > 0


def test_edition_model_name_has_max_length_20(db, edition_fixture):
    reg = edition_fixture(name='a' * 21)
    with assert_raises(ValidationError):
        reg.full_clean()


@mark.skip
def test_edition_model_name_is_unique(db, edition_fixture):
    with assert_raises(IntegrityError):
        reg1 = edition_fixture(name='name test')
        reg2 = edition_fixture(name='name test')


def test_edition_model_name_can_be_blank(db, edition_fixture):
    reg = edition_fixture(name='')
    assert reg.name == ''


def test_edition_model_edition_type_has_max_length_10(db, edition_fixture):
    reg = edition_fixture(edition_type='a' * 11)
    with assert_raises(ValidationError):
        reg.full_clean()


@mark.skip
def test_edition_model_edition_type_db_column_is_type(db, edition_fixture):
    reg = edition_fixture()
    assert hasattr(reg, 'type')


def test_edition_model_theme_has_max_length_100(db, edition_fixture):
    reg = edition_fixture(theme='a' * 101)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_edition_model_theme_can_be_blank(db, edition_fixture):
    reg = edition_fixture(theme='')
    assert reg.theme == ''


def test_edition_model_teams_has_related_name_editions(db, edition_fixture):
    edition_reg = edition_fixture()
    team_reg = Team.objects.first()
    assert isinstance(team_reg.editions.first(), Edition)


def test_edition_model_dunder_str_method_returns_edition_name(db, edition_fixture):
    reg = edition_fixture()
    assert str(reg) == reg.name

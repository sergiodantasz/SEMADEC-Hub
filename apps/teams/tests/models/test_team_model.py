from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import mark
from pytest import raises as assert_raises


def test_team_model_name_has_max_length_75(db, team_fixture):
    reg = team_fixture(name='a' * 76)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_team_model_slug_has_max_length_100(db, team_fixture):
    reg = team_fixture(slug='a' * 101)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_team_model_slug_is_unique(db, team_fixture):
    with assert_raises(IntegrityError):
        team_fixture(slug='test-slug')
        team_fixture(slug='test-slug')


def test_team_model_get_classes_method_returns_correct_value(db, team_fixture):
    reg = team_fixture()
    assert list(reg.get_classes) == list(reg.classes.all())


def test_team_model_get_editions_method_returns_correct_value(db, team_fixture):
    reg = team_fixture()
    assert list(reg.get_editions) == list(reg.editions.all())


def test_team_model_get_edition_team_method_returns_correct_value(db, team_fixture):
    reg = team_fixture()
    assert list(reg.get_edition_team) == list(reg.edition_team.all())


def test_team_model_dunder_str_method_returns_team_name(db, team_fixture):
    reg = team_fixture()
    assert str(reg) == reg.name

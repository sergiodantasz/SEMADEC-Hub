from django.core.exceptions import ValidationError
from pytest import mark
from pytest import raises as assert_raises

# WIP


def test_team_model_name_has_max_length_75(db, team_fixture):
    reg = team_fixture(name='a' * 76)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_team_model_dunder_str_method_returns_team_name(db, team_fixture):
    reg = team_fixture()
    assert str(reg) == reg.name

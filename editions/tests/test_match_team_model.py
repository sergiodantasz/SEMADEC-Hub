from django.core.exceptions import ValidationError
from django.db import IntegrityError
from pytest import mark
from pytest import raises as assert_raises


@mark.skip
def test_match_team_model_score_cannot_be_negative(db, match_team_fixture):
    with assert_raises(IntegrityError):
        reg = match_team_fixture(score=-10)


def test_match_team_model_winner_is_boolean_field(db, match_team_fixture):
    reg = match_team_fixture()
    assert isinstance(reg.winner, bool)


def test_match_team_model_dunder_str_method_returns_team_name(db, match_team_fixture):
    reg = match_team_fixture()
    assert str(reg) == reg.team.name

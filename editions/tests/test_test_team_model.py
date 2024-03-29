from django.db import IntegrityError
from pytest import mark
from pytest import raises as assert_raises


@mark.skip
def test_test_team_model_score_cannot_be_negative(db, test_team_fixture):
    with assert_raises(IntegrityError):
        reg = test_team_fixture(score=-10)


def test_test_team_model_winner_is_boolean_field(db, test_team_fixture):
    reg = test_team_fixture()
    assert isinstance(reg.winner, bool)


def test_test_team_model_dunder_str_method_returns_team_name(db, test_team_fixture):
    reg = test_team_fixture()
    assert str(reg) == reg.team.name

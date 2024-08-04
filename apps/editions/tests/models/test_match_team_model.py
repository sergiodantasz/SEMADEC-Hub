from django.core.exceptions import ValidationError
from django.db import IntegrityError
from pytest import mark
from pytest import raises as assert_raises


def test_match_team_model_score_cannot_be_negative(db, match_team_fixture):
    reg = match_team_fixture(score=-10)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_match_team_model_dunder_str_method_returns_team_name(db, match_team_fixture):
    reg = match_team_fixture()
    assert str(reg) == reg.team.name

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from pytest import mark
from pytest import raises as assert_raises


def test_test_team_model_score_can_be_null(db, test_team_fixture):
    reg = test_team_fixture(score=None)
    assert reg.score is None


def test_test_team_model_dunder_str_method_returns_team_name(db, test_team_fixture):
    reg = test_team_fixture()
    assert str(reg) == reg.team.name

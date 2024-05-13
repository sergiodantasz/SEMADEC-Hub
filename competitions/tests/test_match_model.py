from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises

from competitions.models import Match
from teams.models import Team


def test_match_model_teams_has_related_name_matchs(db, match_fixture):
    match_reg = match_fixture()
    team_reg = Team.objects.first()
    assert isinstance(team_reg.matches.first(), Match)


def test_match_model_scoreboard_max_length_is_10(db, match_fixture):
    reg = match_fixture(scoreboard='a' * 11)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_match_model_date_time_can_be_null(db, match_fixture):
    reg = match_fixture(date_time=None)
    assert reg.date_time is None


def test_match_model_date_time_default_value_is_none(db, match_fixture):
    reg = match_fixture()
    date_time_default = reg._meta.get_field('date_time').get_default()
    assert date_time_default is None


def test_match_model_dunder_str_method_returns_match_sport_name(db, match_fixture):
    reg = match_fixture()
    assert str(reg) == reg.sport.name

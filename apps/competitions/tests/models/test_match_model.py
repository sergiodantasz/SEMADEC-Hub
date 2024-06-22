from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises

from apps.competitions.models import Match
from apps.competitions.tests.factories import MatchFactory, MatchTeamFactory
from apps.teams.models import Team
from apps.teams.tests.factories import TeamFactory


def test_match_model_teams_has_related_name_matchs(db, match_fixture):
    match_reg = match_fixture()
    team_reg = Team.objects.first()
    assert isinstance(team_reg.matches.first(), Match)


def test_match_model_date_time_can_be_null(db, match_fixture):
    reg = match_fixture(date_time=None)
    assert reg.date_time is None


def test_match_model_date_time_default_value_is_none(db, match_fixture):
    reg = match_fixture()
    date_time_default = reg._meta.get_field('date_time').get_default()
    assert date_time_default is None


def test_match_model_get_scoreboard_method_returns_correct_value(db, match_fixture):
    reg = match_fixture()
    desired_out = reg.match_team.values_list('score', flat=True)
    assert list(reg.get_scoreboard) == list(desired_out)


def test_match_model_get_match_teams_display_method_returns_correct_value(
    db, match_fixture
):
    reg = match_fixture()
    desired_out = f'{reg.teams.first()} x {reg.teams.last()}'
    assert reg.get_match_teams_display == desired_out


def test_match_model_dunder_str_method_returns_match_sport_name(db, match_fixture):
    reg = match_fixture()
    desired_out = 'Partida: ' + ' x '.join(team.name for team in reg.teams.all())
    assert str(reg) == desired_out

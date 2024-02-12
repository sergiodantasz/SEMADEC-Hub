def test_team_competition_model_team_db_column_is_team_id(db, team_competition_fixture):
    reg = team_competition_fixture()
    assert hasattr(reg, 'team_id')


def test_team_competition_model_competition_db_column_is_competition_id(
    db, team_competition_fixture
):
    reg = team_competition_fixture()
    assert hasattr(reg, 'competition_id')


def test_team_competition_model_winner_is_boolean_field(db, team_competition_fixture):
    reg = team_competition_fixture()
    assert isinstance(reg.winner, bool)

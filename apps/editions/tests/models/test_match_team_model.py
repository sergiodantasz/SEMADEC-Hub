def test_match_team_model_dunder_str_method_returns_team_name(db, match_team_fixture):
    reg = match_team_fixture()
    assert str(reg) == reg.team.name

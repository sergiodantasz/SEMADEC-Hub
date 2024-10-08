from pytest import mark


def test_edition_team_model_team_db_column_is_team_id(db, edition_team_fixture):
    reg = edition_team_fixture()
    assert hasattr(reg, 'team_id')


def test_edition_team_model_score_can_be_null(db, edition_team_fixture):
    reg = edition_team_fixture(score=None)
    assert reg.score is None


def test_edition_team_model_score_default_value_is_zero(db, edition_team_fixture):
    reg = edition_team_fixture()
    score_default = reg._meta.get_field('score').get_default()
    assert score_default == 0


def test_edition_team_model_dunder_str_method_returns_correct_value(
    db, edition_team_fixture
):
    reg = edition_team_fixture()
    assert str(reg) == f'{reg.team} - {reg.edition}'

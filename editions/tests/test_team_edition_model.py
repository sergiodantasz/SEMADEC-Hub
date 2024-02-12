from pytest import mark


def test_team_edition_model_team_db_column_is_team_id(db, team_edition_fixture):
    reg = team_edition_fixture()
    assert hasattr(reg, 'team_id')


@mark.skip
def test_team_edition_model_edition_db_column_is_edition_year(db, team_edition_fixture):
    reg = team_edition_fixture()
    assert hasattr(reg, 'edition_year')


def test_team_edition_model_score_can_be_null(db, team_edition_fixture):
    reg = team_edition_fixture(score=None)
    assert reg.score is None


@mark.skip
def test_team_edition_model_score_can_be_blank(db, team_edition_fixture):
    reg = team_edition_fixture(score='')
    assert reg.score == ''


def test_team_edition_model_score_default_value_is_none(db, team_edition_fixture):
    reg = team_edition_fixture()
    assert reg.score is None


def test_team_edition_model_classification_can_be_null(db, team_edition_fixture):
    reg = team_edition_fixture(classification=None)
    assert reg.classification is None


@mark.skip
def test_team_edition_model_classification_can_be_blank(db, team_edition_fixture):
    reg = team_edition_fixture(score='')
    assert reg.score == ''


def test_team_edition_model_classification_default_value_is_none(
    db, team_edition_fixture
):
    reg = team_edition_fixture()
    assert reg.score is None

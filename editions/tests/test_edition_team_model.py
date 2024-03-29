from pytest import mark


def test_edition_team_model_team_db_column_is_team_id(db, edition_team_fixture):
    reg = edition_team_fixture()
    assert hasattr(reg, 'team_id')


@mark.skip
def test_edition_team_model_edition_db_column_is_edition_year(db, edition_team_fixture):
    reg = edition_team_fixture()
    assert hasattr(reg, 'edition_year')


def test_edition_team_model_score_can_be_null(db, edition_team_fixture):
    reg = edition_team_fixture(score=None)
    assert reg.score is None


@mark.skip
def test_edition_team_model_score_can_be_blank(db, edition_team_fixture):
    reg = edition_team_fixture(score='')
    assert reg.score == ''


def test_edition_team_model_score_default_value_is_zero(db, edition_team_fixture):
    reg = edition_team_fixture()
    score_default = reg._meta.get_field('score').get_default()
    assert score_default == 0


def test_edition_team_model_classification_can_be_null(db, edition_team_fixture):
    reg = edition_team_fixture(classification=None)
    assert reg.classification is None


@mark.skip
def test_edition_team_model_classification_can_be_blank(db, edition_team_fixture):
    reg = edition_team_fixture(score='')
    assert reg.score == ''


def test_edition_team_model_classification_default_value_is_none(
    db, edition_team_fixture
):
    reg = edition_team_fixture()
    classification_default = reg._meta.get_field('classification').get_default()
    assert classification_default is None

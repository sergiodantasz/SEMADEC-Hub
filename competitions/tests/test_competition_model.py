from pytest import mark


@mark.skip
def test_competition_model_edition_db_column_is_edition_id(
    db, competition_fixture
):  # SEE IT LATER
    reg = competition_fixture()
    assert hasattr(reg, 'edition_id')


def test_competition_model_test_or_sport_db_column_is_test_or_sport_id(
    db, competition_fixture
):
    reg = competition_fixture()
    assert hasattr(reg, 'test_or_sport_id')


def test_competition_model_dunder_str_method_returns_competition_edition_name(
    db, competition_fixture
):
    reg = competition_fixture()
    assert str(reg) == reg.edition.name

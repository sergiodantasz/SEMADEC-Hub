def test_competition_model_edition_db_column_is_edition_id(db, competition_fixture):
    reg = competition_fixture()
    assert hasattr(reg, 'edition_id')

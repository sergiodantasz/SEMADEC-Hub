def test_test_or_sport_test_db_column_is_test_id(db, test_or_sport_fixture):
    reg = test_or_sport_fixture()
    assert hasattr(reg, 'test_id')


def test_test_or_sport_sport_db_column_is_sport_id(db, test_or_sport_fixture):
    reg = test_or_sport_fixture()
    assert hasattr(reg, 'sport_id')

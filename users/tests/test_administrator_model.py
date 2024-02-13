from pytest import mark


@mark.skip
def test_administrator_model_user_db_column_is_user_registration(
    db, administrator_fixture
):
    reg = administrator_fixture()
    assert hasattr(reg, 'user_registration')

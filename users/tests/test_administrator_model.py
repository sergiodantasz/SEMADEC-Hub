from pytest import mark


@mark.skip
def test_administrator_model_user_db_column_is_user_registration(
    db, administrator_fixture
):
    reg = administrator_fixture()
    assert hasattr(reg, 'user_registration')


def test_administrator_model_dunder_str_method_returns_user_name(
    db, administrator_fixture
):
    reg = administrator_fixture()
    assert str(reg) == reg.user.full_name

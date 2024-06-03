def test_sport_category_model_dunder_str_method_returns_sport_and_category_name(
    db, sport_category_fixture
):
    reg = sport_category_fixture()
    assert str(reg) == f'{reg.sport.name} - {reg.category.name}'

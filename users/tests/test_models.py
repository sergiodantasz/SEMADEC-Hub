def test_model_campus_is_correct(db, campus_fixture):
    assert campus_fixture.acronym == 'cn'
    assert campus_fixture.name == 'Currais Novos'

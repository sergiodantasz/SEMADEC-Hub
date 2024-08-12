from django.forms import NumberInput


def test_match_team_form_is_valid(db, match_team_form_fixture):
    form = match_team_form_fixture()
    assert form.is_valid()


def test_match_team_form_score_label_is_correct(db, match_team_form_fixture):
    form = match_team_form_fixture()
    assert form.fields['score'].label == 'Pontuação'


def test_match_team_form_score_widget_is_numberinput(db, match_team_form_fixture):
    form = match_team_form_fixture()
    assert isinstance(form.fields['score'].widget, NumberInput)


def test_match_team_form_score_min_value_is_0(db, match_team_form_fixture):
    form = match_team_form_fixture(score=-10)
    assert not form.is_valid()

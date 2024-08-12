from django.forms import NumberInput


def test_edition_team_form_is_valid(db, edition_team_form_fixture):
    form = edition_team_form_fixture()
    assert form.is_valid()


def test_edition_team_form_score_label_is_correct(db, edition_team_form_fixture):
    form = edition_team_form_fixture()
    assert form.fields['score'].label == 'Pontuação'


def test_edition_team_form_score_widget_is_numberinput(db, edition_team_form_fixture):
    form = edition_team_form_fixture()
    assert isinstance(form.fields['score'].widget, NumberInput)


def test_edition_team_form_score_min_value_is_0(db, edition_team_form_fixture):
    form = edition_team_form_fixture(score=-1)
    assert not form.is_valid()

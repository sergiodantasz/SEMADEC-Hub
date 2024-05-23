from django.forms import (
    NumberInput,
)


def test_test_team_form_score_label_is_correct(db, test_team_form_fixture):
    form = test_team_form_fixture()
    assert form.fields['score'].label == 'Pontuação'


def test_test_team_form_score_widget_is_numberinput(db, test_team_form_fixture):
    form = test_team_form_fixture()
    assert isinstance(form.fields['score'].widget, NumberInput)

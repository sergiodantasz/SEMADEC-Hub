from django.forms import CheckboxSelectMultiple

from apps.teams.models import Class


def test_team_form_is_valid(db, team_form_fixture):
    form = team_form_fixture()
    assert form.is_valid()


def test_team_form_name_max_length_is_75(db, team_form_fixture):
    form = team_form_fixture()
    assert form.fields['name'].max_length == 75


def test_team_form_name_placeholder_is_correct(db, team_form_fixture):
    form = team_form_fixture()
    assert form.fields['name'].widget.attrs['placeholder'] == 'Digite o nome do time...'


def test_team_form_name_label_is_correct(db, team_form_fixture):
    form = team_form_fixture()
    assert form.fields['name'].label == 'Nome'


def test_team_form_classes_queryset_is_correct(db, team_form_fixture):
    form = team_form_fixture()
    assert all(isinstance(reg, Class) for reg in form.fields['classes'].queryset)


def test_team_form_classes_widget_is_checkboxmultiple(db, team_form_fixture):
    form = team_form_fixture()
    assert isinstance(form.fields['classes'].widget, CheckboxSelectMultiple)


def test_team_form_classes_widget_has_html_class(db, team_form_fixture):
    form = team_form_fixture()
    assert form.fields['classes'].widget.attrs['class'] == 'input-checkbox-list'


def test_team_form_classes_label_is_correct(db, team_form_fixture):
    form = team_form_fixture()
    assert form.fields['classes'].label == 'Turmas'

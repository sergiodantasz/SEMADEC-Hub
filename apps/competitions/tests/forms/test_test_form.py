from django.forms import (
    CheckboxSelectMultiple,
    DateTimeInput,
    Textarea,
)

from apps.teams.models import Team


def test_test_form_title_field_placeholder_is_correct(db, test_form_fixture):
    form = test_form_fixture()
    assert (
        form.fields['title'].widget.attrs['placeholder'] == 'Digite o nome da prova...'
    )


def test_test_form_name_max_length_is_50(db, test_form_fixture):
    form = test_form_fixture()
    assert form.fields['title'].max_length == 50


def test_test_form_name_label_is_correct(db, test_form_fixture):
    form = test_form_fixture()
    assert form.fields['title'].label == 'Nome'


def test_test_form_description_field_placeholder_is_correct(db, test_form_fixture):
    form = test_form_fixture()
    assert (
        form.fields['description'].widget.attrs['placeholder']
        == 'Forneça uma breve descrição sobre a prova...'
    )


def test_test_form_description_label_is_correct(db, test_form_fixture):
    form = test_form_fixture()
    assert form.fields['description'].label == 'Descrição'


def test_test_form_description_widget_is_textarea(db, test_form_fixture):
    form = test_form_fixture()
    assert isinstance(form.fields['description'].widget, Textarea)


def test_test_form_description_required_is_false(db, test_form_fixture):
    form = test_form_fixture()
    assert form.fields['description'].required is False


def test_test_form_date_time_widget_is_datetime(db, test_form_fixture):
    form = test_form_fixture()
    assert isinstance(form.fields['date_time'].widget, DateTimeInput)


def test_test_form_date_time_widget_has_html_class(db, test_form_fixture):
    form = test_form_fixture()
    assert form.fields['date_time'].widget.attrs['class'] == 'input-datetime'


def test_test_form_date_time_label_is_correct(db, test_form_fixture):
    form = test_form_fixture()
    assert form.fields['date_time'].label == 'Horário'


def test_test_form_teams_queryset_is_correct(db, test_form_fixture):
    form = test_form_fixture()
    assert all(isinstance(reg, Team) for reg in form.fields['teams'].queryset)


def test_test_form_teams_widget_is_checkboxmultiple(db, test_form_fixture):
    form = test_form_fixture()
    assert isinstance(form.fields['teams'].widget, CheckboxSelectMultiple)


def test_test_form_teams_widget_has_html_class(db, test_form_fixture):
    form = test_form_fixture()
    assert form.fields['teams'].widget.attrs['class'] == 'input-checkbox-list'


def test_test_form_teams_label_is_correct(db, test_form_fixture):
    form = test_form_fixture()
    assert form.fields['teams'].label == 'Times'

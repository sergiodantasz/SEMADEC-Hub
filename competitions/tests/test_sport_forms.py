from django.forms import (
    CheckboxSelectMultiple,
    DateTimeInput,
    NumberInput,
    RadioSelect,
    Textarea,
)

from competitions import forms
from competitions.models import Category, SportCategory
from editions.tests.factories import EditionFactory
from teams.models import Team

# SportForm


def test_sport_form_name_field_placeholder_is_correct(db, sport_form_fixture):
    form = sport_form_fixture()
    assert (
        form.fields['name'].widget.attrs['placeholder'] == 'Digite o nome do esporte...'
    )


def test_sport_form_name_max_length_is_30(db, sport_form_fixture):
    form = sport_form_fixture()
    assert form.fields['name'].max_length == 30


def test_sport_form_name_label_is_correct(db, sport_form_fixture):
    form = sport_form_fixture()
    assert form.fields['name'].label == 'Nome'


def test_sport_form_categories_queryset_is_correct(db, sport_form_fixture):
    form = sport_form_fixture()
    assert all(isinstance(reg, Category) for reg in form.fields['categories'].queryset)


def test_sport_form_categories_widget_is_checkboxmultiple(db, sport_form_fixture):
    form = sport_form_fixture()
    assert isinstance(form.fields['categories'].widget, CheckboxSelectMultiple)


def test_sport_form_categories_widget_has_html_class(db, sport_form_fixture):
    form = sport_form_fixture()
    assert form.fields['categories'].widget.attrs['class'] == 'input-checkbox-list'


def test_sport_form_categories_label_is_correct(db, sport_form_fixture):
    form = sport_form_fixture()
    assert form.fields['categories'].label == 'Categorias'


# TestForm


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


# TestTeamForm


def test_test_team_form_score_label_is_correct(db, test_team_form_fixture):
    form = test_team_form_fixture()
    assert form.fields['score'].label == 'Pontuação'


def test_test_team_form_score_widget_is_numberinput(db, test_team_form_fixture):
    form = test_team_form_fixture()
    assert isinstance(form.fields['score'].widget, NumberInput)


# MatchForm


def test_match_form_if_edition_object_is_given(db, match_form_fixture):
    form = match_form_fixture(edition_obj=EditionFactory())
    ...


def test_match_form_sport_category_queryset_is_correct(db, match_form_fixture):
    form = match_form_fixture()
    assert all(
        isinstance(reg, SportCategory) for reg in form.fields['sport_category'].queryset
    )


def test_match_form_sport_category_widget_is_radioselect(db, match_form_fixture):
    form = match_form_fixture()
    assert isinstance(form.fields['sport_category'].widget, RadioSelect)


def test_match_form_sport_category_label_is_correct(db, match_form_fixture):
    form = match_form_fixture()
    assert form.fields['sport_category'].label == 'Esporte'


def test_match_form_teams_queryset_is_correct(db, match_form_fixture):
    form = match_form_fixture()
    assert all(isinstance(reg, Team) for reg in form.fields['teams'].queryset)


def test_match_form_teams_widget_is_checkboxmultiple(db, match_form_fixture):
    form = match_form_fixture()
    assert isinstance(form.fields['teams'].widget, CheckboxSelectMultiple)


def test_match_form_teams_widget_has_html_class(db, match_form_fixture):
    form = match_form_fixture()
    assert form.fields['teams'].widget.attrs['class'] == 'input-checkbox-list'


def test_match_form_teams_label_is_correct(db, match_form_fixture):
    form = match_form_fixture()
    assert form.fields['teams'].label == 'Times'


def test_match_form_date_time_widget_is_datetimeinput(db, match_form_fixture):
    form = match_form_fixture()
    assert isinstance(form.fields['date_time'].widget, DateTimeInput)


def test_match_form_date_time_widget_has_html_class(db, match_form_fixture):
    form = match_form_fixture()
    assert form.fields['date_time'].widget.attrs['class'] == 'input-datetime'


def test_match_form_date_time_label_is_correct(db, match_form_fixture):
    form = match_form_fixture()
    assert form.fields['date_time'].label == 'Horário'


# MatchTeamForm

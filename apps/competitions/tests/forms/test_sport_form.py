from django.forms import (
    CheckboxSelectMultiple,
)

from apps.competitions.models import Category


def test_sport_form_is_valid(db, sport_form_fixture):
    form = sport_form_fixture()
    assert form.is_valid()


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

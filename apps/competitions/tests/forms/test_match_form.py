from django.forms import (
    CheckboxSelectMultiple,
    DateTimeInput,
    RadioSelect,
)

from apps.competitions.models import SportCategory
from apps.editions.tests.conftest import edition_fixture
from apps.editions.tests.factories import EditionFactory
from apps.teams.models import Team

# def test_match_form_if_edition_object_is_given(db, match_form_fixture):
#     form = match_form_fixture(edition_obj=EditionFactory())
# ...


def test_match_form_set_teams_queryset_updates_teams_queryset(
    db, match_form_fixture, edition_fixture
):
    edition_obj = edition_fixture()
    form = match_form_fixture(edition_obj=edition_obj)
    assert list(form.fields['teams'].queryset) == list(edition_obj.teams.all())


def test_match_form_set_sport_category_queryset_updates_sport_category_queryset(
    db, match_form_fixture, edition_fixture
):
    edition_obj = edition_fixture()
    form = match_form_fixture(edition_obj=edition_obj)
    sport_category_ids = edition_obj.sports.values_list('sport_category', flat=True)
    sport_category_queryset = SportCategory.objects.filter(pk__in=sport_category_ids)
    assert list(form.fields['sport_category'].queryset) == list(sport_category_queryset)


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

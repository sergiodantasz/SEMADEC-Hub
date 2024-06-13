from django.forms import CheckboxSelectMultiple, NumberInput, RadioSelect

from apps.competitions.models import Sport
from apps.teams.models import Team


def test_edition_form_year_placeholder_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert (
        form.fields['year'].widget.attrs['placeholder']
        == 'Digite o ano desta edição...'
    )


def test_edition_form_name_placeholder_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert (
        form.fields['name'].widget.attrs['placeholder']
        == 'Ex: IV Semadec, X Semadec...'
    )


def test_edition_form_theme_placeholder_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert (
        form.fields['theme'].widget.attrs['placeholder']
        == 'Digite o tema desta edição...'
    )


def test_edition_form_year_widget_is_numberinput(db, edition_form_fixture):
    form = edition_form_fixture()
    assert isinstance(form.fields['year'].widget, NumberInput)


def test_edition_form_year_min_value_is_2000(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['year'].widget.attrs['min'] == 2000


def test_edition_form_year_max_value_is_3000(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['year'].widget.attrs['max'] == 3000


def test_edition_form_year_label_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['year'].label == 'Ano'


def test_edition_form_name_max_length_is_20(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['name'].max_length == 20


def test_edition_form_name_label_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['name'].label == 'Nome'


def test_edition_form_edition_type_label_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['edition_type'].label == 'Tipo de Edição'


def test_edition_form_edition_type_widget_is_radioselect(db, edition_form_fixture):
    form = edition_form_fixture()
    assert isinstance(form.fields['edition_type'].widget, RadioSelect)


def test_edition_form_edition_type_widget_has_html_class(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['edition_type'].widget.attrs['class'] == 'input-radio'


def test_edition_form_edition_type_initial_is_courses(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['edition_type'].widget.attrs['class'] == 'input-radio'


def test_edition_form_theme_label_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['theme'].label == 'Tema'


def test_edition_form_theme_max_length_is_100(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['theme'].max_length == 100


def test_edition_form_theme_required_is_false(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['theme'].required is False


def test_edition_form_teams_queryset_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert all(isinstance(reg, Team) for reg in form.fields['teams'].queryset)


def test_edition_form_teams_widget_is_checkboxmultiple(db, edition_form_fixture):
    form = edition_form_fixture()
    assert isinstance(form.fields['teams'].widget, CheckboxSelectMultiple)


def test_edition_form_teams_widget_has_html_class(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['teams'].widget.attrs['class'] == 'input-checkbox-list'


def test_edition_form_teams_label_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['teams'].label == 'Times'


def test_edition_form_sports_queryset_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert all(isinstance(reg, Sport) for reg in form.fields['sports'].queryset)


def test_edition_form_sports_widget_is_checkboxmultiple(db, edition_form_fixture):
    form = edition_form_fixture()
    assert isinstance(form.fields['sports'].widget, CheckboxSelectMultiple)


def test_edition_form_sports_widget_has_html_class(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['sports'].widget.attrs['class'] == 'input-checkbox-list'


def test_edition_form_sports_label_is_correct(db, edition_form_fixture):
    form = edition_form_fixture()
    assert form.fields['sports'].label == 'Esportes'

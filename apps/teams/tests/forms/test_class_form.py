from django.forms import NumberInput, RadioSelect

from apps.teams.models import Course


def test_class_form_is_valid(db, class_form_fixture):
    form = class_form_fixture()
    assert form.is_valid()


def test_class_form_name_placeholder_is_correct(db, class_form_fixture):
    form = class_form_fixture()
    assert (
        form.fields['name'].widget.attrs['placeholder'] == 'Digite o nome da turma...'
    )


def test_class_form_entry_year_placeholder_is_correct(db, class_form_fixture):
    form = class_form_fixture()
    assert (
        form.fields['entry_year'].widget.attrs['placeholder']
        == 'Digite o ano de ingresso da turma...'
    )


def test_class_form_name_max_length_is_30(db, class_form_fixture):
    form = class_form_fixture()
    assert form.fields['name'].max_length == 30


def test_class_form_name_label_is_correct(db, class_form_fixture):
    form = class_form_fixture()
    assert form.fields['name'].label == 'Nome'


# Add tests for entry_year
def test_class_form_entry_year_label_is_correct(db, class_form_fixture):
    form = class_form_fixture()
    assert form.fields['entry_year'].label == 'Ano'


def test_class_form_entry_year_widget_is_numberinput(db, class_form_fixture):
    form = class_form_fixture()
    assert isinstance(form.fields['entry_year'].widget, NumberInput)


def test_class_form_entry_year_min_value_is_2000(db, class_form_fixture):
    form = class_form_fixture()
    assert form.fields['entry_year'].widget.attrs['min'] == 2000


def test_class_form_entry_year_max_value_is_3000(db, class_form_fixture):
    form = class_form_fixture()
    assert form.fields['entry_year'].widget.attrs['max'] == 3000


def test_class_form_course_label_is_correct(db, class_form_fixture):
    form = class_form_fixture()
    assert form.fields['course'].label == 'Curso'


def test_class_form_course_widget_is_radioselect(db, class_form_fixture):
    form = class_form_fixture()
    assert isinstance(form.fields['course'].widget, RadioSelect)


def test_class_form_course_widget_has_html_class(db, class_form_fixture):
    form = class_form_fixture()
    assert form.fields['course'].widget.attrs['class'] == 'input-radio-list'


def test_class_form_course_queryset_is_correct(db, class_form_fixture):
    form = class_form_fixture()
    assert all(isinstance(reg, Course) for reg in form.fields['course'].queryset)

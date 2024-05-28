from django.forms import CheckboxSelectMultiple
from django.forms.widgets import RadioSelect

from teams.models import Class, Course


def test_course_form_is_valid(db, course_form_fixture):
    form = course_form_fixture()
    assert form.is_valid()


def test_course_form_name_placeholder_is_correct(db, course_form_fixture):
    form = course_form_fixture()
    assert (
        form.fields['name'].widget.attrs['placeholder'] == 'Digite o nome do curso...'
    )


def test_course_form_name_max_length_is_75(db, course_form_fixture):
    form = course_form_fixture()
    assert form.fields['name'].max_length == 75


def test_course_form_name_label_is_correct(db, course_form_fixture):
    form = course_form_fixture()
    assert form.fields['name'].label == 'Nome'


def test_class_form_is_valid(db, class_form_fixture):
    form = class_form_fixture()
    assert form.is_valid()


def test_class_form_name_placeholder_is_correct(db, class_form_fixture):
    form = class_form_fixture()
    assert (
        form.fields['name'].widget.attrs['placeholder'] == 'Digite o nome da turma...'
    )


def test_class_form_name_max_length_is_30(db, class_form_fixture):
    form = class_form_fixture()
    assert form.fields['name'].max_length == 30


def test_class_form_name_label_is_correct(db, class_form_fixture):
    form = class_form_fixture()
    assert form.fields['name'].label == 'Nome'


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

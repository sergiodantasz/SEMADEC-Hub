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

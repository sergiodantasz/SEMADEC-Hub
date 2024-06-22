from pytest import mark


def test_tag_form_is_valid(db, tag_form_fixture):
    form = tag_form_fixture()
    assert form.is_valid()


def test_tag_form_name_max_length_is_50(db, tag_form_fixture):
    form = tag_form_fixture()
    assert form.fields['name'].max_length == 50


def test_tag_form_name_label_is_correct(db, tag_form_fixture):
    form = tag_form_fixture()
    assert form.fields['name'].label == 'Nome'


def test_tag_form_name_has_unique_error_message(db, tag_form_fixture):
    form = tag_form_fixture()
    assert (
        form.fields['name'].error_messages['unique']
        == 'Uma tag com este nome já foi criada.'
    )


def test_tag_form_clean_name_method_returns_name(db, tag_form_fixture):
    form = tag_form_fixture()
    form.full_clean()
    method = form.clean_name()
    assert method == form.cleaned_data['name']

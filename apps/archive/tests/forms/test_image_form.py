def test_image_form_images_field_multiple_is_true(db, image_form_fixture):
    form = image_form_fixture()
    assert form.fields['images'].widget.attrs['multiple'] is True


def test_image_form_images_field_hidden_is_true(db, image_form_fixture):
    form = image_form_fixture()
    assert form.fields['images'].widget.attrs['hidden'] is True


def test_image_form_images_required_is_false(db, image_form_fixture):
    form = image_form_fixture()
    assert form.fields['images'].required is False

from django.core.files import File
from django.forms import CheckboxSelectMultiple, FileInput, HiddenInput
from pytest import mark

from apps.competitions import forms
from apps.home.models import Tag


@mark.skip
def test_image_collection_form_is_valid(db, image_collection_form_fixture):
    form = image_collection_form_fixture()
    form.full_clean()
    assert form.is_valid()


def test_image_collection_form_title_field_placeholder_is_correct(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert (
        form.fields['title'].widget.attrs['placeholder']
        == 'Digite o título da coleção...'
    )


def test_image_collection_form_cover_widget_is_fileinput(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert isinstance(form.fields['cover'].widget, FileInput)


def test_image_collection_form_cover_label_is_correct(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert form.fields['cover'].label == 'Capa'


def test_image_collection_form_cover_required_is_false(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert form.fields['cover'].required is False


def test_image_collection_form_cover_is_hidden(db, image_collection_form_fixture):
    form = image_collection_form_fixture()
    assert form.fields['cover'].widget.attrs['hidden'] is True


def test_image_collection_form_title_has_max_length_200(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert form.fields['title'].max_length == 200


def test_image_collection_form_title_label_is_correct(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert form.fields['title'].label == 'Título'


def test_image_collection_form_collection_type_widget_is_hiddeninput(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert isinstance(form.fields['collection_type'].widget, HiddenInput)


def test_image_collection_form_collection_type_initial_is_image(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert form.fields['collection_type'].initial == 'image'


def test_image_collection_form_tags_queryset_is_correct(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert all(isinstance(reg, Tag) for reg in form.fields['tags'].queryset)


def test_image_collection_form_tags_widget_is_checkboxmultiple(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert isinstance(form.fields['tags'].widget, CheckboxSelectMultiple)


def test_image_collection_form_tags_required_is_false(
    db, image_collection_form_fixture
):
    form = image_collection_form_fixture()
    assert form.fields['tags'].required is False


def test_image_collection_form_tags_label_is_correct(db, image_collection_form_fixture):
    form = image_collection_form_fixture()
    assert form.fields['tags'].label == 'Tags'


def test_image_collection_form_clean_name_method_returns_error_if_no_cover_provided(
    db, image_collection_form_fixture, image_fixture
):
    image = image_fixture()[0]
    form = image_collection_form_fixture()
    form.full_clean()
    form.cleaned_data['cover'] = image.content
    response = form.clean_cover()
    assert isinstance(response, File)

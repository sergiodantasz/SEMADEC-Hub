from django.forms import CheckboxSelectMultiple, HiddenInput

from apps.home.models import Tag


def test_document_collection_form_title_placeholder_is_correct(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert (
        form.fields['title'].widget.attrs['placeholder']
        == 'Digite o título da coleção...'
    )


def test_document_collection_form_title_max_length_is_200(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert form.fields['title'].max_length == 200


def test_document_collection_form_title_label_is_correct(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert form.fields['title'].label == 'Título'


def test_document_collection_form_collection_type_widget_is_hiddeninput(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert isinstance(form.fields['collection_type'].widget, HiddenInput)


def test_document_collection_form_collection_type_initial_is_document(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert form.fields['collection_type'].initial == 'document'


def test_document_collection_form_tags_queryset_is_correct(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert all(isinstance(reg, Tag) for reg in form.fields['tags'].queryset)


def test_document_collection_form_tags_widget_is_checkboxmultiple(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert isinstance(form.fields['tags'].widget, CheckboxSelectMultiple)


def test_document_collection_form_tags_widget_has_html_class(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert (
        form.fields['tags'].widget.attrs['class'] == 'tags-checkbox-list'
    )  # change to 'input-checkbox-list'


def test_document_collection_form_tags_required_is_false(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert form.fields['tags'].required is False


def test_document_collection_form_tags_label_is_correct(
    db, document_collection_form_fixture
):
    form = document_collection_form_fixture()
    assert form.fields['tags'].label == 'Tags'

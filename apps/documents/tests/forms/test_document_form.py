def test_document_form_is_valid(db, document_form_fixture):
    form = document_form_fixture()
    assert form.is_valid()


def test_document_form_documents_multiple_is_true(db, document_form_fixture):
    form = document_form_fixture()
    assert form.fields['documents'].widget.attrs['multiple'] is True


def test_document_form_documents_hidden_is_true(db, document_form_fixture):
    form = document_form_fixture()
    assert form.fields['documents'].widget.attrs['hidden'] is True


def test_document_form_documents_required_is_false(db, document_form_fixture):
    form = document_form_fixture()
    assert form.fields['documents'].required is False

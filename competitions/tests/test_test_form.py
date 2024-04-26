from competitions import forms


def test_test_form_title_field_placeholder_is_correct():
    form = forms.TestForm()
    assert (
        form.fields['title'].widget.attrs['placeholder'] == 'Digite o nome da prova...'
    )


def test_test_form_description_field_placeholder_is_correct():
    form = forms.TestForm()
    assert (
        form.fields['description'].widget.attrs['placeholder']
        == 'Forneça uma breve descrição sobre a prova...'
    )

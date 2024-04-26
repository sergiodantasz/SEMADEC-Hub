from competitions import forms


def test_sport_form_name_field_placeholder_is_correct():
    form = forms.SportForm()
    assert (
        form.fields['name'].widget.attrs['placeholder'] == 'Digite o nome do esporte...'
    )

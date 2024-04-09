from django import forms

from helpers.form import set_attr, set_placeholder
from home.models import Collection


class DocumentCollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['title'], 'Digite o título da coleção...')

    class Meta:
        model = Collection
        fields = ['title', 'collection_type']  # Add tags

    title = forms.CharField(
        max_length=200,
        label='Título',
    )
    collection_type = forms.CharField(
        widget=forms.HiddenInput(),
        initial='document',
    )


class DocumentForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_attr(self.fields['documents'], 'multiple', True)
        set_attr(self.fields['documents'], 'hidden', True)

    documents = forms.FileField(
        required=False,
    )

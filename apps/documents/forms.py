from django import forms

from apps.home.models import Collection, Tag
from helpers.form import set_attr, set_placeholder


class DocumentCollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['title'], 'Digite o título da coleção...')

    class Meta:
        model = Collection
        fields = ['title', 'collection_type', 'tags']

    title = forms.CharField(
        max_length=200,
        label='Título',
    )
    collection_type = forms.CharField(
        widget=forms.HiddenInput(),
        initial='document',
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.order_by('name'),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'tags-checkbox-list'},
        ),
        required=False,
        label='Tags',
    )


class DocumentForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_attr(self.fields['documents'], 'multiple', True)
        set_attr(self.fields['documents'], 'hidden', True)

    documents = forms.FileField(
        required=False,
    )

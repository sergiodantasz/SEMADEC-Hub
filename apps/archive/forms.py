from django import forms

from apps.home.models import Collection, Tag
from helpers.form import set_attr, set_placeholder


class ImageCollectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_attr(self.fields['cover'], 'hidden', True)
        set_placeholder(self.fields['title'], 'Digite o título da coleção...')

    class Meta:
        model = Collection
        fields = ['cover', 'title', 'collection_type', 'tags']

    cover = forms.ImageField(
        widget=forms.FileInput(),
        required=False,
        label='Capa',
    )
    title = forms.CharField(
        max_length=200,
        label='Título',
    )
    collection_type = forms.CharField(
        widget=forms.HiddenInput(),
        initial='image',
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.order_by('name'),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'tags-checkbox-list'},
        ),
        required=False,
        label='Tags',
    )

    def clean_cover(self):
        cover = self.cleaned_data['cover']
        if cover is None:
            self.add_error('cover', 'A capa é obrigatória.')
        return cover


class ImageForm(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_attr(self.fields['images'], 'multiple', True)
        set_attr(self.fields['images'], 'hidden', True)

    images = forms.ImageField(
        required=False,
    )

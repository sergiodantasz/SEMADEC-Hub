from string import punctuation

from django import forms

from apps.home.models import Tag


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tag
        fields = ['name']

    name = forms.CharField(
        max_length=50,
        label='Nome',
        error_messages={
            'unique': 'Uma tag com este nome já foi criada.',
        },
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        for p in punctuation:
            if p in name:
                self.add_error('name', 'O nome da tag não pode conter pontuação.')
        return name

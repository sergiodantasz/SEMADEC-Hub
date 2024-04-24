from django import forms

from home.models import Tag


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

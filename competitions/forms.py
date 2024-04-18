from django import forms

from competitions.models import Category, Sport, Test
from editions.models import Team
from helpers.form import set_attr, set_placeholder


class SportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['name'], 'Digite o nome do esporte...')

    class Meta:
        model = Sport
        fields = ['name', 'categories']

    name = forms.CharField(
        max_length=30,
        label='Nome',
        required=True,
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Categorias',
        required=True,
    )


class TestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['title'], 'Digite o nome da prova...')
        set_placeholder(
            self.fields['description'], 'Forneça uma breve descrição sobre a prova...'
        )

    class Meta:
        model = Test
        fields = ['title', 'description', 'date_time', 'teams']

    title = forms.CharField(
        max_length=50,
        label='Nome',
    )
    description = forms.CharField(
        label='Descrição',
        widget=forms.Textarea,
        required=False,
    )
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Horário',
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Times',
    )
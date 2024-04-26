from django import forms

from competitions.models import Category, Sport, Test, TestTeam
from editions.models import Team
from helpers.form import set_attr, set_placeholder


class SportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['name'], 'Digite o nome do esporte...')

    class Meta:
        model = Sport
        # fields = '__all__'
        exclude = ['slug']

    name = forms.CharField(
        max_length=30,
        label='Nome',
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'input-checkbox-list'},
        ),
        label='Categorias',
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
        # fields = '__all__'
        exclude = ['slug']

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
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'input-datetime',
            }
        ),
        label='Horário',
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'input-checkbox-list'},
        ),
        label='Times',
    )


class TestTeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    class Meta:
        model = TestTeam
        fields = ['score']

    score = forms.CharField(
        label='Pontuação',
        widget=forms.NumberInput(),
    )

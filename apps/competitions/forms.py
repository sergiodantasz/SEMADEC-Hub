from django import forms

from apps.competitions.models import (
    Category,
    Match,
    MatchTeam,
    Sport,
    SportCategory,
    Test,
    TestTeam,
)
from apps.teams.models import Team
from helpers.form import set_placeholder


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


class MatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        edition_obj = kwargs.get('edition_obj', '')
        if edition_obj:
            kwargs.pop('edition_obj')
        super().__init__(*args, **kwargs)
        if edition_obj:
            self.set_sport_category_queryset(edition_obj)
            self.set_teams_queryset(edition_obj)

    def set_teams_queryset(self, edition_obj):
        self.fields['teams'].queryset = edition_obj.teams.all()

    def set_sport_category_queryset(self, edition_obj):
        sport_category_ids = edition_obj.sports.values_list('sport_category', flat=True)
        sport_category_queryset = SportCategory.objects.filter(
            pk__in=sport_category_ids
        )
        self.fields['sport_category'].queryset = sport_category_queryset

    class Meta:
        model = Match
        fields = ['sport_category', 'date_time', 'teams']

    sport_category = forms.ModelChoiceField(
        queryset=SportCategory.objects.all(),  # Review it later
        widget=forms.RadioSelect(
            attrs={'class': 'input-radio-list'},
        ),
        label='Esporte',
    )

    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),  # Review it later
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'input-checkbox-list'},
        ),
        label='Times',
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


class MatchTeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    class Meta:
        model = MatchTeam
        fields = ['score']

    score = forms.CharField(
        label='Pontuação',
        widget=forms.NumberInput(),
    )

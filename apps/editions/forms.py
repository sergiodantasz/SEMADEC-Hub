from django import forms
from django.db.models import Q
from django.forms.models import BaseModelFormSet

from apps.competitions.models import Sport
from apps.editions.models import Edition, EditionTeam
from apps.teams.models import Team
from helpers.form import set_attr, set_placeholder


class EditionForm(forms.ModelForm):
    EDITION_TYPE_CHOICES = (
        ('courses', 'Confronto entre cursos'),
        ('classes', 'Confronto entre turmas'),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['year'], 'Digite o ano desta edição...')
        set_placeholder(self.fields['name'], 'Ex: IV Semadec, X Semadec...')
        set_placeholder(self.fields['theme'], 'Digite o tema desta edição...')

    class Meta:
        model = Edition
        fields = ['year', 'name', 'edition_type', 'theme', 'sports', 'teams']

    year = forms.CharField(
        label='Ano',
        widget=forms.NumberInput(attrs={'min': 2000, 'max': 3000}),
    )
    name = forms.CharField(
        label='Nome',
        max_length=20,
    )
    edition_type = forms.ChoiceField(
        label='Tipo de Edição',
        choices=EDITION_TYPE_CHOICES,
        widget=forms.RadioSelect(
            attrs={'class': 'input-radio'},
        ),
        initial='courses',
    )
    theme = forms.CharField(
        label='Tema',
        max_length=100,
        required=False,
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'input-checkbox-list'},
        ),
        label='Times',
    )
    sports = forms.ModelMultipleChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'input-checkbox-list'},
        ),
        label='Esportes',
    )


class EditionTeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    class Meta:
        model = EditionTeam
        fields = ['score']

    score = forms.CharField(
        label='Pontuação',
        widget=forms.NumberInput(),
    )

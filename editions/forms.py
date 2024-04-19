from tkinter import Widget

from django import forms
from django.db.models import Q

from editions.models import EditionTeam
from helpers.form import set_attr, set_placeholder

from .models import Edition, Team


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
        fields = [
            'year',
            'name',
            'edition_type',
            'theme',
            'teams',
        ]

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


class EditionTeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    class Meta:
        model = EditionTeam
        fields = ['score', 'classification']

    # team = forms.CharField()
    score = forms.CharField(
        label='Pontuação',
        widget=forms.NumberInput(),
    )
    classification = forms.CharField(
        label='Classificação',
        widget=forms.NumberInput(),
    )


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    class Meta:
        model = EditionTeam
        fields = ['name']

    name = forms.CharField(
        max_length=75,
    )

from django import forms

from helpers.form import set_placeholder
from teams.models import Class, Course, Team


class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['name'], 'Digite o nome do time...')

    class Meta:
        model = Team
        fields = ['name', 'classes']

    name = forms.CharField(
        max_length=75,
        label='Nome',
    )
    classes = forms.ModelMultipleChoiceField(
        queryset=Class.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'input-checkbox-list'},
        ),
        label='Turmas',
    )


class ClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['name'], 'Digite o nome da turma...')

    class Meta:
        model = Class
        fields = ['name', 'course']

    name = forms.CharField(
        max_length=30,
        label='Nome',
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),  # Review it later
        widget=forms.RadioSelect(
            attrs={'class': 'input-radio-list'},
        ),
        label='Curso',
    )


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['name'], 'Digite o nome do curso...')

    class Meta:
        model = Course
        fields = ['name']

    name = forms.CharField(
        max_length=75,
        label='Nome',
    )

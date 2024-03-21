from django import forms

from .models import Collection


class SubmitArchiveForm(forms.ModelForm):
    class Meta:
        model = Collection
        # fields = ['title', 'files', 'cover']
        fields = ['title', 'files']

    files = forms.FileField()

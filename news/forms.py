from django import forms
from django_summernote.widgets import SummernoteWidget

from helpers.form import set_attr, set_placeholder
from home.models import Tag
from news.models import News


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_attr(self.fields['cover'], 'hidden', True)
        set_placeholder(self.fields['title'], 'Digite o título da notícia...')
        set_placeholder(self.fields['excerpt'], 'Digite o título do excerto...')

    class Meta:
        model = News
        fields = ['cover', 'title', 'excerpt', 'content', 'tags']

    cover = forms.ImageField(
        widget=forms.FileInput(),
        required=False,
        label='Capa',
    )
    title = forms.CharField(
        max_length=200,
        label='Título',
    )
    excerpt = forms.CharField(
        max_length=200,
        label='Excerto',
    )
    content = forms.CharField(
        widget=SummernoteWidget(),
        label='Conteúdo',
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.order_by('name'),
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'tags-checkbox-list'},
        ),
        required=False,
        label='Tags',
    )

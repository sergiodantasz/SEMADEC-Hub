from django import forms
from django_summernote.widgets import SummernoteWidget

from helpers.form import set_placeholder
from news.models import News


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        set_placeholder(self.fields['title'], 'Digite o título da notícia...')
        set_placeholder(self.fields['excerpt'], 'Digite o título do excerto...')

    class Meta:
        model = News
        fields = ['cover', 'title', 'excerpt', 'content']

    cover = forms.ImageField(
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

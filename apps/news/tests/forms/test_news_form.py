from django.forms import CheckboxSelectMultiple, FileInput
from django_summernote.widgets import SummernoteWidget

from apps.home.models import Tag


def test_news_form_is_valid(db, news_form_fixture):
    form = news_form_fixture()
    assert form.is_valid()


def test_news_form_cover_hidden_is_true(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['cover'].widget.attrs['hidden'] is True


def test_news_form_title_placeholder_is_correct(db, news_form_fixture):
    form = news_form_fixture()
    assert (
        form.fields['title'].widget.attrs['placeholder']
        == 'Digite o título da notícia...'
    )


def test_news_form_excerpt_placeholder_is_correct(db, news_form_fixture):
    form = news_form_fixture()
    assert (
        form.fields['excerpt'].widget.attrs['placeholder']
        == 'Digite o título do excerto...'
    )


def test_news_form_cover_widget_is_fileinput(db, news_form_fixture):
    form = news_form_fixture()
    assert isinstance(form.fields['cover'].widget, FileInput)


def test_news_form_cover_required_is_false(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['cover'].required is False


def test_news_form_cover_label_is_correct(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['cover'].label == 'Capa'


def test_news_form_title_max_length_is_200(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['title'].max_length == 200


def test_news_form_title_label_is_correct(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['title'].label == 'Título'


def test_news_form_excerpt_max_length_is_200(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['excerpt'].max_length == 200


def test_news_form_excerpt_label_is_correct(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['excerpt'].label == 'Excerto'


def test_news_form_content_widget_is_summernotewidget(db, news_form_fixture):
    form = news_form_fixture()
    assert isinstance(form.fields['content'].widget, SummernoteWidget)


def test_news_form_content_label_is_correct(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['content'].label == 'Conteúdo'


def test_news_form_tags_queryset_is_correct(db, news_form_fixture):
    form = news_form_fixture()
    assert all(isinstance(reg, Tag) for reg in form.fields['tags'].queryset)


def test_news_form_tags_widget_is_checkboxmultiple(db, news_form_fixture):
    form = news_form_fixture()
    assert isinstance(form.fields['tags'].widget, CheckboxSelectMultiple)


def test_news_form_tags_required_is_false(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['tags'].required is False


def test_news_form_tags_label_is_correct(db, news_form_fixture):
    form = news_form_fixture()
    assert form.fields['tags'].label == 'Tags'

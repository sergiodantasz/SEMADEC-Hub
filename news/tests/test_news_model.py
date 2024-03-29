from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import mark
from pytest import raises as assert_raises

from home.models import Tag
from news.models import News


def test_news_model_administrator_db_column_is_administrator_id(db, news_fixture):
    reg = news_fixture()
    assert hasattr(reg, 'administrator_id')


def test_news_model_title_has_max_length_200(db, news_fixture):
    reg = news_fixture(title='a' * 201)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_news_model_excerpt_has_max_length_200(db, news_fixture):
    reg = news_fixture(excerpt='a' * 201)
    with assert_raises(ValidationError):
        reg.full_clean()


@mark.skip
def test_news_model_slug_has_max_length_225(db, news_fixture):
    reg = news_fixture(slug='a' * 226)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_news_model_slug_is_unique(db, news_fixture):
    with assert_raises(IntegrityError):
        reg1 = news_fixture(slug='test-slug')
        reg2 = news_fixture(slug='test-slug')


def test_news_model_tags_has_related_name_news(db, news_fixture):
    news_reg = news_fixture()
    tag_reg = Tag.objects.first()
    assert isinstance(tag_reg.news.first(), News)


def test_news_model_dunder_str_method_returns_news_title(db, news_fixture):
    reg = news_fixture()
    assert str(reg) == reg.title

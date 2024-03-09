import datetime

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import mark
from pytest import raises as assert_raises


def test_document_model_administrator_db_column_is_administrator_id(
    db, document_fixture
):
    reg = document_fixture()
    assert hasattr(reg, 'administrator_id')


def test_document_model_title_has_max_length_200(db, document_fixture):
    reg = document_fixture(title='a' * 201)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_document_model_content_is_unique(db, document_fixture):
    with assert_raises(IntegrityError):
        reg1 = document_fixture(content='conteudo')
        reg2 = document_fixture(content='conteudo')


@mark.skip
def test_document_model_content_db_column_is_path(db, document_fixture):
    reg = document_fixture()
    assert hasattr(reg, 'path')


def test_document_model_slug_has_max_length_225(db, document_fixture):
    reg = document_fixture(slug='a' * 226)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_document_model_slug_is_unique(db, document_fixture):
    with assert_raises(IntegrityError):
        reg1 = document_fixture(slug='test-slug')
        reg2 = document_fixture(slug='test-slug')


def test_document_model_dunder_str_method_returns_document_title(db, document_fixture):
    reg = document_fixture()
    assert str(reg) == reg.title

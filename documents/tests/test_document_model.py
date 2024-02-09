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


def test_document_model_slug_has_maxlength_225(db, document_fixture):
    ...


@mark.skip
def test_document_model_created_at_cannot_be_edited(db, document_fixture):
    reg = document_fixture()
    reg.created_at = eval(
        'datetime.datetime(2024, 2, 8, 18, 2, 18, 598321, tzinfo=datetime.timezone.utc)'
    )
    reg.full_clean()

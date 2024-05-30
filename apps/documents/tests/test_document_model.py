from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises

from apps.documents.models import Document
from apps.home.models import Collection


def test_document_model_collection_fk_points_to_collection_model(db, document_fixture):
    reg = document_fixture()[0]
    assert isinstance(reg.collection, Collection)


def test_document_model_name_has_max_length_100(db, document_fixture):
    reg = document_fixture(name='a' * 101)[0]
    with assert_raises(ValidationError):
        reg.full_clean()


def test_document_model_content_path_is_correct(db, document_fixture):
    reg = document_fixture()[0]
    assert 'collections/document/files' in reg.content.url


def test_document_model_dunder_str_method_returns_document_name(db, document_fixture):
    reg = document_fixture()[0]
    assert str(reg) == reg.name

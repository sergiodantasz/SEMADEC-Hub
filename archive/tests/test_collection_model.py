from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_collection_model_administrator_db_column_is_administrator_id(
    db, collection_fixture
):
    reg = collection_fixture()
    assert hasattr(reg, 'administrator_id')


def test_collection_model_title_has_max_length_200(db, collection_fixture):
    reg = collection_fixture(title='a' * 201)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_collection_model_title_is_unique(db, collection_fixture):
    with assert_raises(IntegrityError):
        reg1 = collection_fixture(title='Coleção Teste')
        reg2 = collection_fixture(title='Coleção Teste')


def test_collection_model_cover_default_value_is_placeholder(db, collection_fixture):
    reg = collection_fixture()
    assert reg.cover == '/base/static/global/img/collection_cover_placeholder.jpg'


def test_collection_model_slug_is_unique(db, collection_fixture):
    with assert_raises(IntegrityError):
        reg1 = collection_fixture(slug='test-slug')
        reg2 = collection_fixture(slug='test-slug')


def test_collection_model_slug_has_max_length_225(db, collection_fixture):
    reg = collection_fixture(slug='a' * 226)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_collection_model_created_at_cannot_be_updated(db, collection_fixture):
    reg = collection_fixture(created_at='01/01/2020')
    reg.created_at = '02/01/2020'
    with assert_raises(ValidationError):
        reg.full_clean()

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_file_model_collection_db_column_is_collection_id(db, file_fixture):
    reg = file_fixture()
    assert hasattr(reg, 'collection_id')


def test_file_model_content_is_unique(db, file_fixture):
    with assert_raises(IntegrityError):
        reg1 = file_fixture(content='/test/fixture.py')
        reg1 = file_fixture(content='/test/fixture.py')

from django.core.exceptions import ValidationError
from pytest import raises as assert_raises


def test_collection_model_title_has_max_length_200(db, collection_fixture):
    collection = collection_fixture(title='a' * 201)
    with assert_raises(ValidationError):
        collection.full_clean()

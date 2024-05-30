from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises

from apps.archive.models import Image
from apps.home.models import Collection


def test_image_model_collection_fk_points_to_collection_model(db, image_fixture):
    reg = image_fixture()[0]
    assert isinstance(reg.collection, Collection)


def test_image_model_content_path_is_correct(db, image_fixture):
    reg = image_fixture()[0]
    assert 'collections/image/files' in reg.content.url


def test_image_dunder_str_method_returns_image_content_name(db, image_fixture):
    reg = image_fixture()[0]
    assert str(reg) == reg.content.name

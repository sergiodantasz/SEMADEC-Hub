from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_category_model_name_has_max_length_15(db, category_fixture):
    reg = category_fixture(name='a' * 16)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_category_model_name_is_primary_key(db, category_fixture):
    reg = category_fixture()
    assert reg.pk == reg.name


def test_category_model_get_css_class_getter_returns_class_name(db, category_fixture):
    reg = category_fixture()
    assert (reg.get_css_class).startswith('category-tag-')


def test_category_model_dunder_str_method_returns_category_name(db, category_fixture):
    reg = category_fixture()
    assert str(reg) == reg.name

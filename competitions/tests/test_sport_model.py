from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.db.utils import IntegrityError
from pytest import mark
from pytest import raises as assert_raises

from competitions.models import Category, Sport


def test_sport_model_name_has_max_length_30(db, sport_fixture):
    reg = sport_fixture(name='a' * 31)
    with assert_raises(ValidationError):
        reg.full_clean()


@mark.skip
def test_sport_model_category_db_column_is_category_id(db, sport_fixture):
    reg = sport_fixture()
    assert hasattr(reg, 'category_id')


def test_sport_model_get_categories_getter_returns_categories_queryset(
    db, sport_fixture
):
    reg = sport_fixture()
    assert isinstance(reg.get_categories, QuerySet)


def test_sport_model_get_files_getter_returns_only_file_model_objects(
    db, sport_fixture
):
    reg = sport_fixture()
    categories = reg.get_categories
    assert all(isinstance(cat, Category) for cat in categories)


def test_sport_model_categories_has_related_name_sports(db, sport_fixture):
    sport_reg = sport_fixture()
    categories_reg = Category.objects.first()
    assert isinstance(categories_reg.sports.first(), Sport)


def test_sport_model_dunder_str_method_returns_sport_name(db, sport_fixture):
    reg = sport_fixture()
    assert str(reg) == reg.name

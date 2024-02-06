from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_test_model_title_has_max_length_50(db, test_fixture):  # Review it later
    reg = test_fixture(title='a' * 51)
    with assert_raises(ValidationError):
        reg.full_clean()

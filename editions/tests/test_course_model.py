from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises


def test_course_model_name_has_max_length_75(db, course_fixture):
    reg = course_fixture(name='a' * 76)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_course_model_name_is_unique(db, course_fixture):
    with assert_raises(IntegrityError):
        reg1 = course_fixture(name='name test')
        reg2 = course_fixture(name='name test')

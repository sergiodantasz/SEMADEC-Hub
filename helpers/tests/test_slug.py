from django.utils.text import slugify

from apps.teams.tests.factories import CourseFactory
from helpers import slug


def test_generate_random_characters_returns_str_object():
    func = slug.generate_random_characters()
    assert isinstance(func, str)


def test_generate_random_characters_uses_k_parameter():
    func = slug.generate_random_characters(k=10)
    assert len(func) == 10


def test_generate_random_characters_default_k_value_is_5():
    func = slug.generate_random_characters()
    assert len(func) == 5


def test_generate_slug_returns_str_object():
    func = slug.generate_slug(string='Test String')
    assert isinstance(func, str)


def test_generate_dynamic_slug_returns_str_object(db):
    course = CourseFactory()
    func = slug.generate_dynamic_slug(course, 'slug')
    assert isinstance(func, str)

from pytest import raises as assert_raises

from helpers import random_


def test_generate_random_string_function_returns_str_object():
    func = random_.generate_random_string()
    assert isinstance(func, str)


def test_generate_random_string_function_uses_k_parameter():
    func = random_.generate_random_string(k=10)
    assert len(func) == 10


def test_generate_random_string_function_default_k_value_is_64():
    func = random_.generate_random_string()
    assert len(func) == 64


def test_generate_random_string_function_raises_typeerror_if_k_is_not_int():
    with assert_raises(TypeError):
        random_.generate_random_string(k=None)

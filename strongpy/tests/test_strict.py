import pytest

from strongpy import strict
from strongpy.utils.exceptions import \
    ParameterTypeError, \
    ReturnTypeError, \
    NonKwargInDecoratorError, \
    ParameterTypehintMissingError


@strict()
def only_strings(a: str, b: str) -> str:
    return a + b


@strict
def wrong_return_type(a: str, b: int) -> float:
    return a * b


@strict(force_parameter_typehints=False)
def no_annotations(a, b):
    return a + b


@strict(force_parameter_typehints=False)
def some_annotations(a, b: int) -> int:
    return a * b


@strict(force_parameter_typehints=False)
def few_annotations(a: int, b):
    return a + b


def test_correct():
    only_strings("a string", "a second string")
    no_annotations(4, 2)
    some_annotations(4, 2)


def test_wrong_parameter_type():
    with pytest.raises(TypeError):
        no_annotations("4", 2)
    with pytest.raises(TypeError):
        no_annotations("4", 2)

    with pytest.raises(ParameterTypeError):
        only_strings("a string", 42)
    with pytest.raises(ParameterTypeError):
        some_annotations(4, "2")
    with pytest.raises(ParameterTypeError):
        few_annotations("4", 2)


def test_not_enough_args():
    with pytest.raises(TypeError):
        only_strings("only one string")
    with pytest.raises(TypeError):
        no_annotations(4)
    with pytest.raises(TypeError):
        some_annotations(4)
    with pytest.raises(TypeError):
        few_annotations(4)


def test_to_many_args():
    with pytest.raises(TypeError):
        only_strings("a string", "another string", "what is this?")
    with pytest.raises(TypeError):
        no_annotations(4, 2, 0)
    with pytest.raises(TypeError):
        some_annotations(4, 2, 0)
    with pytest.raises(TypeError):
        few_annotations(4, 2, 0)


def test_wrong_return_type():
    with pytest.raises(ReturnTypeError):
        some_annotations("4", 2)
    with pytest.raises(ReturnTypeError):
        wrong_return_type("a string", 42)


def test_non_kwarg_definition():
    with pytest.raises(NonKwargInDecoratorError):
        @strict(1)
        def no_kwargs(a, b):
            return a + b


def test_missing_typehints():
    with pytest.raises(ParameterTypehintMissingError):
        @strict()
        def no_annotations(a, b):
            return a * b

from inspect import getfullargspec, _is_type as is_type
from strongpy.utils.constants import TYPE_TUPLE, TYPE_UNION
from typing import Union

from .types import UnspecifiedType, UnionType
from .exceptions import NonKwargInDecoratorError


class FunctionSpecifications:
    def __init__(self, function):
        argspec = getfullargspec(function)

        self.typehints = generate_typehints(function)
        self.args = argspec.args


def generate_typehints(func):
    argspec = getfullargspec(func)

    td = {}
    for arg in argspec.args:
        type_annotation = argspec.annotations.get(arg, UnspecifiedType)
        td[arg] = unpack_type(type_annotation)

    return_annotation = argspec.annotations.get("return", UnspecifiedType)
    td["return"] = unpack_type(return_annotation)

    return td


def construct_args_dict(argnames, args, kwargs):
    args_dict = {}

    left_args = [arg for arg in argnames]

    # Align all keywordless arguments
    for name, arg in zip(argnames, args):
        args_dict[name] = arg
        left_args.remove(name)

    for key, value in kwargs.items():
        args_dict[key] = value

    return args_dict


def unpack_type(packed_type):
    """ Takes a type annotation and converts it into a meaningful type or tuple
        of types.
        - If the annotation was no type, returns a tuple of UnspecifiedType
        - If the annotation was a single type, returns (type, )
        - If the annotation was a Union of types, returns (typeA, typeB, ...)
        type_tuple = (UnspecifiedType,)
    """

    type_tuple = (UnspecifiedType, )

    if type(packed_type) == UnionType:
        # Unions guarantee, that their args are types. No further checks
        # are required.
        type_tuple = packed_type.__args__
    elif is_type(packed_type):
        type_tuple = (packed_type, )
    else:
        pass

    return type_tuple


def has_proper_type(obj, target_type):
    """ Decides whether a given object matches the given target type / target
        type union or not.
    """
    # Unpack the type to a tuple. If it was a Union all types are listed in the
    # tuple.
    types = unpack_type(target_type)

    # Check for each type in types if it matches, break if so.
    is_proper = False
    for t in types:
        if isinstance(obj, t):
            is_proper = True
            break

    return is_proper


def is_clean_decorator(args_obj, kwargs_obj):
    """ Checks whether a decorator is used directly and without passing
        arguments. If passing arguments, they *must* be keyworded, otherwise a
        `NonKwargInDecorator` will be raised.

        An example that returns `True`:
        ```
        @decorator
        def function():
            pass
        ```

        An example that returns `False`:
        ```
        @decorator(mode="fast",sorting="ascending",method=3)
        def function():
            pass
        ```

        Another example that returns `False`:
        ```
        @decorator()
        def function():
            pass
        ```

        An example that raises an `Exception`:
        ```
        @decorator(42)
        def function():
            pass
        ```
    """

    # If no non-keyword argument is passed, we do not care how many keyworded
    # arguments are passed -> The decorator is not clean.
    if len(args_obj) == 0:
        return False
    # If one and only one non-keyword argument is passed, it must be the
    # function to be wrapped and no keywords are allowed.
    elif len(args_obj) == 1 and callable(args_obj[0]) and kwargs_obj == dict():
        return True
    # More than one non-keyword argument or mixed non-keyword and keyword
    # arguments are never valid.
    else:
        raise NonKwargInDecoratorError(args_obj)

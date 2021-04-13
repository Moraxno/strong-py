from typing import Union


class UnspecifiedType:
    """ Custom Type that signals an argument without designated typing.
    """

    pass


""" Type of Unions
"""
UnionType = type(Union[str, int])

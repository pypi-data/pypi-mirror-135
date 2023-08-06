# interval.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2021 Róbert Čerňanský



""":class:`Interval` class."""



__all__ = ["Interval"]



# {{{ INCLUDES

from numbers import Number
from typing import TypeVar, Generic

# }}} INCLUDES



# {{{ CLASSES

T = TypeVar("T", bound=Number)



class Interval(Generic[T]):
    """Interval of numbers.

    :param min: The lower bound.
    :param max: The upper bound."""

    def __init__(self, min: T, max: T):
        self.__min = min
        self.__max = max



    @property
    def min(self) -> T:
        "Lower bound."

        return self.__min



    @property
    def max(self) -> T:
        "Upper bound."

        return self.__max

# }}} CLASSES

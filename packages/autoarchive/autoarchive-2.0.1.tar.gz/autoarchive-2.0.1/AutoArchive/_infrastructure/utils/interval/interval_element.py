# interval_element.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2021 Róbert Čerňanský



""":class:`IntervalElement` class."""



__all__ = ["IntervalElement"]



# {{{ INCLUDES

from .interval import Interval

# }}} INCLUDES



# {{{ CLASSES

class IntervalElement:
    """An element from a numeric interval.

    It is possible to specify value outside of the defined interval.  The behavior is undefined in this case.

    :param value: The number from ``interval``.
    :param interval: The interval the ``value`` is from."""

    def __init__(self, value: int, interval: Interval[int]):
        self.__value = value
        self.__interval = interval



    @property
    def value(self) -> int:
        "Value of the element."

        return self.__value



    def remapTo(self, targetInterval: Interval[int]):
        """Returns new element which is this element remapped to a target interval.

        Examples:

            element = 5, self.__interval = <0, 10>, targetInterval = <0, 100> => 50
            element = 9, self.__interval = <1, 9>, targetInterval = <1, 19> => 19

        :param targetInterval:  Interval which this element shall be remapped to.
        :return: Element from the target interval ``targetInterval``."""

        return IntervalElement(
            round(((self.value - self.__interval.min) / (self.__interval.max - self.__interval.min))
                  * (targetInterval.max - targetInterval.min)) + targetInterval.min,
            targetInterval)

# }}} CLASSES

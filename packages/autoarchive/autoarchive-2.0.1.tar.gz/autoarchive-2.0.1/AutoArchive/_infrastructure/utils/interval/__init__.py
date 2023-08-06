# __init__.py
#
# Project: AutoArchive
# License: GNU GPLv3
#
# Copyright (C) 2003 - 2021 Róbert Čerňanský



"""Operations with interval of integers."""



from .interval import *
from .interval_element import *



__all__ = interval.__all__ + interval_element.__all__

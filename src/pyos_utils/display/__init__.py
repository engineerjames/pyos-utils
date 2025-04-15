from collections.abc import Callable

from ._factory import DisplayInterfaceFactory
from ._interface import DisplayInterface

get_display: Callable[..., DisplayInterface] = DisplayInterfaceFactory.create_interface

__all__ = [
    "DisplayInterface",
    "get_display",
]

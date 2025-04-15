from collections.abc import Callable

from ._display_interface import DisplayInterface
from ._factory import DisplayInterfaceFactory

get_display: Callable[..., DisplayInterface] = DisplayInterfaceFactory.create_interface

__all__ = [
    "DisplayInterface",
    "get_display",
]
